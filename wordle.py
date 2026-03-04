import csv
import random
import numpy as np

def getAnswers():
    possibleAnswers = []
    with open('valid_guesses.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            possibleAnswers.append(row)
        return [answer[0] for answer in possibleAnswers]

def getAnswer(possibleAnswers):
    return random.choice(possibleAnswers)


def checkGuess(currentGuess, answer):
    response = ""

    for guessLetter, answerLetter in zip(currentGuess, answer):
        if (guessLetter == answerLetter):
            response = response + "3"
        elif (guessLetter in answer):
            response = response + "2"
        else:
            response = response + "1"

    return response

def removeAnswersWithRating1(possibleAnswers, response, prevGuess):
    possibleAnswersCopy = possibleAnswers.copy()
    for prevGuessLetter, responseNum in zip(prevGuess, response):
        if (responseNum == "1"):
            possibleAnswersCopy = [possibleAnswer for possibleAnswer in possibleAnswersCopy if prevGuessLetter not in possibleAnswer]
           # print(possibleAnswersCopy[-10:])
    #print(possibleAnswersCopy[-10:])
    return possibleAnswersCopy

def rateAnswers(possibleAnswers, response, prevGuess):
    answersAndRatings = []
    for possibleAnswer in possibleAnswers:
        skip = False
        rating = []
        for i in range(5):
            if possibleAnswer[i] == prevGuess[i] and response[i] == "3":
                rating.append(3)
            elif (possibleAnswer[i] in prevGuess) and (possibleAnswer[i] != prevGuess[i]) and response[i] == "2":
                rating.append(2)
            elif (possibleAnswer[i] == prevGuess[i]) and response[i] == "2":
                skip = True
                break
            else:
                rating.append(1)
        if skip:
            continue
        else:
            answersAndRatings.append((possibleAnswer, rating))


    print(answersAndRatings[-10:])
    return answersAndRatings


def chooseGuess(answersAndRatings):
    bestGuess = ""
    bestRating = 0
    for possibleAnswer, rating in answersAndRatings:
        ratingSum = np.sum(rating)
        if ratingSum > bestRating:
            bestGuess = possibleAnswer
            bestRating = ratingSum

    return bestGuess

    
if __name__ == '__main__':
    possibleAnswers = getAnswers()
    answer = getAnswer(possibleAnswers)
   # answer = "zymic"
    print(answer)

    for i in range(6):
        currentGuess = input("Guess: ")
        response = checkGuess(currentGuess, answer)
        if (response == "33333"):
            print("You win!")
            break
        else:
            print(response)
            possibleAnswers = removeAnswersWithRating1(possibleAnswers, response, currentGuess)
            answersAndRatings = rateAnswers(possibleAnswers, response, currentGuess)
            bestGuess = chooseGuess(answersAndRatings)
            print("Best guess: ", bestGuess)