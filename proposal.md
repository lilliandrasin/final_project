# Proposal

## What will (likely) be the title of your project?

Texas Hold'em Simulation Guide

## In just a sentence or two, summarize your project. (E.g., "A website that lets you buy and sell stocks.")

A program that simulates a Texas Hold'em hand, analyzing pre-flop strategy and post-flop odds and outs to guide the player's betting decisions.

## In a paragraph or more, detail your project. What will your software do? What features will it have? How will it be executed?

This program plays one Texas Hold’em hand from preflop through river using: functions, loops, lists, dictionaries, random, simple text to show calculations and pygame for card graphics.
It builds a 52-card deck, deals hole cards, and advances street by street (preflop --> flop--> turn --> river). At each street it prints the game state and key numbers that guide decisions: pot size, amount to call, pot odds, required equity, estimated win probability, and the expected value  of FOLD, CALL, and RAISE. Preflop behavior is modeled by a basic preflop range given by the preflop chart of the 169 unique hands. The program then recommends an action and accepts the user’s choice. It updates the state dictionary (pot, to_call, street, etc.) and either continues or ends on a fold. Cards are shown as strings like “As” or “Td, as well as graphics. Equity may be computed with a small Monte Carlo sample.


## If planning to combine 1051's final project with another course's final project, with which other course? And which aspect(s) of your proposed project would relate to 1051, and which aspect(s) would relate to the other course?

N/A

## If planning to collaborate with 1 or 2 classmates for the final project, list their names, email addresses, and the names of their assigned TAs below.

N/A

## In the world of software, most everything takes longer to implement than you expect. And so it's not uncommon to accomplish less in a fixed amount of time than you hope.

### In a sentence (or list of features), define a GOOD outcome for your final project. I.e., what WILL you accomplish no matter what?

I will definitely accomplish the actual game program and calculations. 

### In a sentence (or list of features), define a BETTER outcome for your final project. I.e., what do you THINK you can accomplish before the final project's deadline?

- Card graphics
- Bluffing logic

### In a sentence (or list of features), define a BEST outcome for your final project. I.e., what do you HOPE to accomplish before the final project's deadline?

The best outcome for this project would have it include the features listed above in addition to the actual game/calculation aspect.

## In a paragraph or more, outline your next steps. What new skills will you need to acquire? What topics will you need to research? If working with one of two classmates, who will do what?

My next steps is to understand how to create a dictionary for the ranges, learning about the calculations used to properly determine the odds/probabilities, getting a better grasp on continuosly updating dictionaries, and familiarizing myself with pygame library as I've never done anything with graphics. 

I also need to ensure that my program is as efficient and organized as possible, i.e. where/when to call the functions, incorporating a "main" loop of some sort, and organizational techniques to make the code look clean and easy to follow.
