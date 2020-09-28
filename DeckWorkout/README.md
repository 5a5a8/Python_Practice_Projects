# DeckWorkout
Simple program to create workouts inspired by the 'Deck of Cards Workout'.

This was written in September 2020 as a tool for my own personal use. As such it currently does not have things like input validation. It will break if you use it incorrectly in its current state.

I used to do a workout using a deck of cards and described in more detail at http://rosstraining.com/blog/deck-of-cards/
After a while I wanted to add more customisability. I wanted to have more than four exercises and have different rep ranges than a deck of cards offered.

In the deck of cards workout, you might have Spades = Pushups. Each time you drew a spade, you'd do as many pushups as the number on the card. So a 9 of spades would be 9 pushups, and you'd end up working from 2 reps (2 of spades) through 14 reps (Ace of spades) by the time you finished the deck.

In the workouts.csv file, you specify a name for the workout and then exercises and a rep range. If we wanted to replicate a deck of cards we'd use something like:
Example Name, Spades/2-14|Clubs/2-14|Hearts/2-14|Diamonds/2-14

Or we can create something custom:
Example Name, Pushups/5-20|Squats/1-12|Kettlebell Swings/1-10|30 Seconds Jump Rope/2-6

You can add as many exercises as you want and whatever sort of rep range you want.
You can add workouts in the workouts.csv file directly or you can use the built-in functionality.
