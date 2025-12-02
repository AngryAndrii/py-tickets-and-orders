from typing import Any

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import UniqueConstraint


# from tests.test_main import movie_sessions_data


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class User(AbstractUser):
    pass


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Movie(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    actors = models.ManyToManyField(to=Actor, related_name="movies")
    genres = models.ManyToManyField(to=Genre, related_name="movies")

    def __str__(self) -> str:
        return self.title


class CinemaHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self) -> str:
        return self.name


class MovieSession(models.Model):
    show_time = models.DateTimeField()
    cinema_hall = models.ForeignKey(
        to=CinemaHall, on_delete=models.CASCADE, related_name="movie_sessions"
    )
    movie = models.ForeignKey(
        to=Movie, on_delete=models.CASCADE, related_name="movie_sessions"
    )

    def __str__(self) -> str:
        return f"{self.movie.title} {str(self.show_time)}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name="orders"
    )

    def __str__(self) -> str:
        return f"Order: {self.created_at}"

    class Meta:
        ordering = ["-created_at"]


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    movie_session = models.ForeignKey(
        to=MovieSession, on_delete=models.CASCADE, related_name="tickets"
    )
    order = models.ForeignKey(
        to=Order, on_delete=models.CASCADE, related_name="tickets"
    )

    def __str__(self) -> str:
        return (
            f"Ticket: "
            f"{self.movie_session.movie.title} "
            f"{self.movie_session.show_time} "
            f"(row: {self.row}, seat: {self.seat})"
        )

    def clean(self) -> None:
        if (
                0 >= self.row > self.movie_session.cinema_hall.rows
                or 0 >= self.seat
                > self.movie_session.cinema_hall.seats_in_row
        ):
            raise ValueError(
                f"Seat myst be in range [1, "
                f"{self.movie_session.cinema_hall.seats_in_row}], "
                f"not {self.seat}, "
                f"and row must be in range"
                f" [1, {self.movie_session.cinema_hall.rows}], "
                f"not {self.row}")

    def save(self, *args, **kwargs) -> Any:
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        constraints = [
            UniqueConstraint(name="unique_ticket",
                             fields=["row", "seat", "movie_session"])
        ]
