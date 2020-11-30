# Secret Santa

An app to text people with secret santa stuff.

## Assumptions

1. That there is a solution (will keep going until it finds one)
2. You have a first and last name
3. The input data is of good quality
4. The Phone Numbers are from the `US` Region
5. That you're me and are using the data I put in

## Rules

There are a few rules in the engine:

1. You don't get your partner (users Partner ID)
2. You don't end up with a cycle (A has B and B has A)
3. You don't get yourself

## `user-list.csv` format

|Field Name|Description|Type|
|----------|-----------|----|
|`ID`|Sequential ID|integer|
|`Name`|The person's name|string|
|`Phone`|The person's phone number|string|
|`Relation ID`|A reference to the person's partner|null or integer|

## Environment Variables

|Name|Description|
|----|-----------|
|`TWILIO_ACCOUNT_SID`|The Account SID for your Paid Twilio.com account|
|`TWILIO_AUTH_TOKEN`|The Production Auth Token for your Paid Twilio.com account|
|`TWILIO_FROM`|The `from` number, that you own in Twilio, in e164 format|
