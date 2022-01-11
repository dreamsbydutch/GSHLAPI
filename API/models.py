from sqlalchemy import Column, Integer, Numeric, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("NOW()"))


class Position(Base):
    __tablename__ = "positions"
    id = Column(Integer, primary_key=True, nullable=False)
    position = Column(String, nullable=False)


class Week(Base):
    __tablename__ = "weeks"
    id = Column(Integer, primary_key=True, nullable=False)
    week_number = Column(Integer, nullable=False)
    season = Column(Integer, nullable=False)
    start_date = Column(TIMESTAMP(timezone=True), nullable=False)
    end_date = Column(TIMESTAMP(timezone=True), nullable=False)
    number_of_days = Column(Integer, nullable=False)
    season_type = Column(String, nullable=False)


class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, nullable=False)
    team_name = Column(String, nullable=False)
    team_logo = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")
    conference = Column(String, nullable=False)


class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    nhl_team = Column(String, nullable=False)
    gshl_team_id = Column(Integer, ForeignKey(
        "teams.id", ondelete="CASCADE"), nullable=False)
    gshl_team = relationship("Team")
    salary = Column(Integer, nullable=False)
    rating = Column(Numeric, nullable=False)


class PlayerDailyStats(Base):
    __tablename__ = "player_daily_stats"
    id = Column(Integer, primary_key=True, nullable=False)
    player_id = Column(Integer, ForeignKey(
        "players.id", ondelete="CASCADE"), nullable=False)
    player = relationship("Player")
    team_id = Column(Integer, ForeignKey(
        "teams.id", ondelete="CASCADE"), nullable=False)
    team = relationship("Team")
    week_id = Column(Integer, ForeignKey(
        "weeks.id", ondelete="CASCADE"), nullable=False)
    week = relationship("Week")
    goals = Column(Integer)
    assists = Column(Integer)
    points = Column(Integer)
    plus_minus = Column(Integer)
    penalty_minutes = Column(Integer)
    powerplay_points = Column(Integer)
    shots = Column(Integer)
    hits = Column(Integer)
    blocks = Column(Integer)
    wins = Column(Integer)
    goals_against_avg = Column(Numeric)
    save_percentage = Column(Numeric)
    shutouts = Column(Integer)
    goals_against = Column(Integer)
    saves = Column(Integer)
    shots_against = Column(Integer)
    time_on_ice = Column(Numeric)


class PlayerPosition(Base):
    __tablename__ = "player_position"
    player_id = Column(ForeignKey(
        "players.id", ondelete="CASCADE"), primary_key=True)
    position_id = Column(ForeignKey(
        "positions.id", ondelete="CASCADE"), primary_key=True)


class TeamWeeklyStats(Base):
    __tablename__ = "team_weekly_stats"
    id = Column(Integer, primary_key=True, nullable=False)
    team_id = Column(Integer, ForeignKey(
        "teams.id", ondelete="CASCADE"), nullable=False)
    team = relationship("Team")
    week_id = Column(Integer, ForeignKey(
        "weeks.id", ondelete="CASCADE"), nullable=False)
    week = relationship("Week")
    goals = Column(Integer)
    assists = Column(Integer)
    points = Column(Integer)
    plus_minus = Column(Integer)
    penalty_minutes = Column(Integer)
    powerplay_points = Column(Integer)
    shots = Column(Integer)
    hits = Column(Integer)
    blocks = Column(Integer)
    wins = Column(Integer)
    goals_against_avg = Column(Numeric)
    save_percentage = Column(Numeric)
    shutouts = Column(Integer)
    goals_against = Column(Integer)
    saves = Column(Integer)
    shots_against = Column(Integer)
    time_on_ice = Column(Numeric)


# class Matchups(Base):
#     __tablename__ = "matchups"
#     id = Column(Integer, primary_key=True, nullable=False)
#     week_id = Column(Integer, ForeignKey(
#         "weeks.id", ondelete="CASCADE"), nullable=False)
#     week = relationship("Week")
#     conf_type = Column(String)
#     home_team_id = Column(Integer, ForeignKey(
#         "teams.id", ondelete="CASCADE"), nullable=False)
#     home_team = relationship("Team")
#     home_team_win_loss = Column(String)
#     home_team_score = Column(Integer)
#     home_team_rank = Column(Integer)
#     home_team_stats_id = Column(Integer, ForeignKey(
#         "team_weekly_stats.id", ondelete="SET NULL"))
#     home_team_stats = relationship("TeamWeeklyStats")
#     away_team_id = Column(Integer, ForeignKey(
#         "teams.id", ondelete="CASCADE"), nullable=False)
#     away_team = relationship("Team")
#     away_team_win_loss = Column(String)
#     away_team_score = Column(Integer)
#     away_team_rank = Column(Integer)
#     away_team_stats_id = Column(Integer, ForeignKey(
#         "team_weekly_stats.id", ondelete="SET NULL"))
#     away_team_stats = relationship("TeamWeeklyStats")
