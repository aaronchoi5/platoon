# Platoon
## Rules
There are two different types of cards: Regular cards and Special cards
Regular cards are those from the two to the queen. These are called the pawns. The cards from two to nine are wrth their face value, while the ten, jack and queen are each worth ten. 

![pic](https://github.com/aaronchoi5/platoon/blob/master/frontend/src/assets/cardspic.PNG)

Special Cards, meanwhile, come in three varieties: kings, bishops, and wizards. 

If you have a king in your unit you will always win, regardless of the unit's total value. But if there are two units facing each other, both having kings, the unit with the highest total value of regular cards will win.

If you have a bishop in your unit you will always lose. There is one exception to this. If the opposing unit contains a king, then a unit containing a bishop will win. If two units containing bishops face each other, the one with the highest value of regular cards will win, much like when two units with kings do battle.

Wizard cards swap your unit with your opponent's unit. You cannot have a unit with just only a wizard and wizards have a value of zero.

The maximum number of special cards that can be in a single unit is two.

In addition, you cannot include a king and a bishop in the same unit.

## Setting Up the Server and Website