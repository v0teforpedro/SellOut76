# SellOut76
 
#### Video Demo:  https://www.youtube.com/watch?v=RQglRJeV2BQ
 
This web-app was created to help out "Fallout 76" players manage their weapon inventory, as well as finding new weapons for their own collection.
 
 
Technologies used:
 
- Python
- JavaScript (Jquery)
- Flask
- Bootstrap 4
- sqlite3
- HTML
- CSS
 
 
## How does the webpage work?
 
User registers. During registration you need to enter these fields:
 
- Name
- Reddit name
- Password: it is checked to match, must be 8-20 symbols long, with at least one uppercase character and  number, is hashed after checks are done
 
 
After registration the user is redirected to the homepage (index.html). At homepage users will see a greeting, and explanation of web-app purpose, and description of other available actions they can perfom within this web-app.
 
 
 
**Add:**
 
Allows the user to select type of weapon (melee or ranged), when type is selected hidden dropdown list appears with 4 additional select boxes and submit button. These dropdowns are dependent on weapon type and they change dynamically (achieved with Jquery and Flask's Jsonify), it prevents users from selecting unobtainable weapons (with features not applicable for it's type). When the user clicks the submit button, the app checks which fields were selected, and if this select is correct. If it's not correct (could be because the user forgot mandatory selections), with the help of the "apology" function, it renders an error as a picture with error code and description. If everything is correct, the user is being redirected to "inventory.html" where a flash message will inform which item has been added.
 
**Inventory:**
 
It represents a datatable, with weapons and their corresponding features that user previously added. On top of the table there is a search box, which listens for the user's input, and searches through data entries in the table (excluding table head). Table consists of 5 columns, 4 of which represent data, and the last one is an "action" column with delete button. Users are able to delete any entry from the personal table. If a row has been deleted, the webpage will redirect the user to inventory.html with an updated table, prompting the user with a flash message which item was removed.
 
**Search:**
 
Search.html will look the same as the dropdown list of add.html, with less restriction of user selection. Only type is mandatory to select, other fields can be left untouched. This was made to let users browse through inventories of other registered users. Basically, a user can make a strict request for a specific item (by selecting all prefixes), or can search just by item type, or name, or one of the prefixes. Search will exclude user's own weapons, so only other users items will be displayed in result.
 
Result of the search request will be rendered as result.html. It looks similar to an inventory table, but with different color style, and without the delete option - instead of which is a column with the reddit name of the item owner. This way our user will know who to contact in order to settle potential trade deals regarding wanted items.
 
### Routing
 
Each route checks if the user is authenticated. It means if username and password were supplied, all changes to inventory will be made by the corresponding user.
 
### Sessions
 
The webpage uses sessions to confirm that the user is registered. Once the user logins, his credentials are checked with the database. Once everything passes a session is created and stored in the cookies.
 
### Database
 
Database has 6 tables:
- users: which contains id, username, password hash and redditname columns
- weapons: which contains id, name of the weapon, class (created for future app development), and type
- mainp (represents main prefix): which contains id, name, description, type
- majorp (represents major prefix): which contains id, name, description, type
- minorp (represents minor prefix): which contains id, name, description, type
- user_weapons: contains own id and weapon_id, main_id, major_id, minor_id as foreign keys referencing previous tables.
 
So the most interesting part here is that we keep data of users' weapons (which will be the one to grow as users add more and more items) in integers only, and reference them through JOIN queries to other tables.
 
## Future development
 
I can see this web app as my pet project, which can be used by all players of this huge MMORPG.
When this web-app goes live, I plan to implement following features:
 
- Add proper registration with email, as well add the ability to fast log in by using a reddit account and their API.
- Ability to change account details, add email notifications
- Add same options we have for weapons, to armor segment of the game
- Implementation of "Auction" through web-app, let users set a price and list items
- Add chat and message service within web-app
 
## How to launch application
 
1. Check that you have Python version 3.9.6+
2. Clone the code
3. Install all dependencies
4. Run Flask
6. You are ready to go!
