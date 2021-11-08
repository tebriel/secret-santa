#!/usr/bin/env python
"""Secret Santa SMS Application."""
import os
import csv
import random
from typing import List, Optional
from dataclasses import dataclass

import phonenumbers
from twilio import rest
client = rest.Client()


@dataclass
class Person:
    """Data object to represent a person from the csv file."""

    user_id: int
    name: str
    phone_number: str
    relation_id: Optional[int]
    match_id: Optional[int]


def main():
    """Run the program, notify people of their match."""
    matches = generate_matches()
    with open('./matches.txt', 'w', encoding='utf-8') as outfile:
        for match in matches:
            outfile.write(f'{match[0].name} gets {match[1].name}\n')
    for match in matches:
        print(f'Sending {match[0].name} their Match!')
        sms_match(*match)


def sms_match(dest: Person, match: Person):
    """Send an SMS to a person letting them know who they have."""
    first_name = dest.name.split()[0]
    match_first_name = match.name.split()[0]
    client.messages.create(
        to=dest.phone_number,
        from_=os.getenv('TWILIO_FROM', ''),
        body=f'''
Hey {first_name}, it's Secret Santa Time 🤫 🎅 🕑 !
You've been matched with {match_first_name}!
Get them something pretty and be prepared to receive a 🎁 from your Santa!
''')


def generate_matches() -> List[List[Person]]:
    """Loop until we get a set of valid matches."""
    while True:
        try:
            matched: List[Person] = []
            results: List[List[Person]] = []
            people = load_file()
            for person in people:
                match = match_person(person, people, matched)
                matched.append(match)
                results.append([person, match])
            return results
        except IndexError:
            pass


def match_person(
    person: Person,
    people: List[Person],
    matched: List[Person],
) -> Person:
    """Match a person, following the rules."""
    def filter_func(x: Person) -> bool:
        if x.user_id == person.user_id:
            return False
        if x.user_id == person.relation_id:
            return False
        if x.relation_id == person.user_id:
            return False
        if x.match_id == person.user_id:
            return False
        if x in matched:
            return False
        return True

    possibles = list(filter(filter_func, people))
    match = random.choice(possibles)
    person.match_id = match.user_id
    return match


def load_file() -> List[Person]:
    """Load and parse the CSV."""
    results = []
    with open('./user-list.csv', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            relation_id: Optional[int]
            if row['Relation ID']:
                relation_id = int(row['Relation ID'])
            else:
                relation_id = None
            parsed_num = phonenumbers.parse(row['Phone'], 'US')
            formatted_num = phonenumbers.format_number(
                parsed_num,
                phonenumbers.PhoneNumberFormat.E164
            )
            results.append(
                Person(
                    user_id=int(row['ID']),
                    name=row['Name'],
                    phone_number=formatted_num,
                    relation_id=relation_id,
                    match_id=None
                )
            )
    return results


if __name__ == '__main__':
    main()
