CREATE DATABASE IF NOT EXISTS rrp;

USE rrp;

DROP TABLE IF EXISTS Users;
CREATE TABLE Users(
    Username varchar(64) NOT NULL,
    Password varchar(255) NOT NULL,
    Email varchar(255) NOT NULL,
    Role varchar(64) CHECK (Role='admin' OR Role='user'),
    PRIMARY KEY (Username)
);


DROP TABLE IF EXISTS Books;
CREATE TABLE Books(
    ISBN13 varchar(13) NOT NULL,
    Title varchar(256) NOT NULL,
    Author varchar(256) NOT NULL,
    Description text,
    Publisher varchar(256) NOT NULL,
    PublishedDate datetime NOT NULL,
    Language varchar(64),
    GoogleRating float,
    PRIMARY KEY (ISBN13)
);

DROP TABLE IF EXISTS BookGenres;
CREATE TABLE BookGenres(
    ISBN13 varchar(13) NOT NULL,
    Genre varchar(128) NOT NULL,
    FOREIGN KEY (ISBN13) REFERENCES Books(ISBN13)
);

DROP TABLE IF EXISTS UserCollections;
CREATE TABLE UserCollections(
    Username varchar(64) NOT NULL,
    ISBN13 varchar(13) NOT NULL,
    CreationTime datetime NOT NULL,
    Name varchar(128) NOT NULL,
    FOREIGN KEY (Username) REFERENCES Users(Username),
    FOREIGN KEY (ISBN13) REFERENCES Books(ISBN13)
);


DROP TABLE IF EXISTS BookReviews;
CREATE TABLE BookReviews(
    Username varchar(64) NOT NULL,
    ISBN13 varchar(13) NOT NULL,
    Rating float NOT NULL CHECK (Rating <= 5 and Rating >= 0),
    Review text,
    ReviewTime datetime,
    FOREIGN KEY (Username) REFERENCES Users(Username),
    FOREIGN KEY (ISBN13) REFERENCES Books(ISBN13)
)
