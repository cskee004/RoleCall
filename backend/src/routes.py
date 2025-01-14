from flask import (Blueprint, request, jsonify)
from db import get_db_connection
import hashlib
import mysql.connector
from matching_algorithm import match_listings
import logging

main = Blueprint("main",__name__)

@main.route('/listings/<int:userId>', methods=['GET'])
def get_user_listings(userId):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM UserListings WHERE userProfileId = %s",(userId,))
    listings = cursor.fetchall()
    conn.close()
    return jsonify(listings)

@main.route('/listings', methods=['POST'])
def save_user_listings():
    data = request.get_json()
    
    required_fields = ["campaign", "gameName", "environment", "day", "startTime", "endTime", "difficulty", "role", "userProfileId"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "INSERT INTO UserListings (campaign, gameName, environment, day, startTime, endTime, difficulty, role, userProfileId)"
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (
            data["campaign"],
            data["gameName"],
            data["environment"],
            data["day"],
            data["startTime"],
            data["endTime"],
            data["difficulty"],
            data["role"],
            data["userProfileId"]
        )
    )
    conn.commit()
    listing_id = cursor.lastrowid
    conn.close()

    return jsonify({"message": "Listing saved", "listing_id": listing_id}),201

@main.route('/listings', methods=['PUT'])
def update_user_listings():
    data = request.get_json()
    required_fields = ["campaign", "gameName", "environment", "day", "startTime", "endTime", "difficulty", "role", "userProfileId"]
    for field in required_fields:
        if field not in data:
            print(field)
            return jsonify({"error": f"Missing required field: {field}"}), 400
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    print(data["campaign"])
    cursor.execute("SELECT * FROM UserListings WHERE userProfileId = %s AND campaign = %s AND gameName = %s",(
        data["userProfileId"],
        data["campaign"],
        data["gameName"]))

    row = cursor.fetchone()

    if not row:
        return jsonify({"error": "Listing Not Found"}),404
    
    listing_id = row['id']

    cursor.execute(
        "UPDATE UserListings "
        "SET campaign = %s, gameName = %s, environment = %s, day = %s, "
        "startTime = %s, endTime = %s, difficulty = %s, role = %s, userProfileId = %s "
        "WHERE id = %s",
        (
            data["campaign"],
            data["gameName"],
            data["environment"],
            data["day"],
            data["startTime"],
            data["endTime"],
            data["difficulty"],
            data["role"],
            data["userProfileId"],
            listing_id
        )
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Listing Updated", "listingid": listing_id}),201

@main.route('/users/<string:name>', methods=['GET'])
def get_user_profile_id(name):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id FROM UserProfiles WHERE name = %s",(name,))
    user_id = cursor.fetchall()
    conn.close()
    return jsonify(user_id)

@main.route('/matches', methods=['GET'])
def get_match_listings():
    listId = request.args.get("listingId")
    userId = request.args.get("userId")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM UserListings WHERE id = %s", (listId,))
    being_matched = cursor.fetchone()
    cursor.execute("SELECT * FROM UserListings WHERE userProfileId != %s",(userId,))
    compare_listings = cursor.fetchall()
    conn.close()
    results = match_listings(compare_listings, being_matched)
    if not results:
        return "None"
    return results

@main.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM UserProfiles;')
    users = cursor.fetchall()
    conn.close()
    return jsonify(users)

@main.route('/register', methods=['GET'])
def set_users():
    conn=get_db_connection()

    username = request.args.get('username')
    password = request.args.get('password')
    email = request.args.get('email')
    password=hashlib.sha256(password.encode()).hexdigest()

    cursor = conn.cursor(dictionary=True)
    cursor.execute('INSERT INTO UserProfiles (name,password,email) VALUES (%s, %s, %s);', (username,password,email))
    conn.commit()
    conn.close()

    response = {
        "message": f"Hello, {username}. Your password is {password}, your email is {email}."
    }
    return jsonify(response)

@main.route('/login', methods=['GET'])
def check_users():
    conn=get_db_connection()

    username = request.args.get('username')
    password = request.args.get('password')
    password=hashlib.sha256(password.encode()).hexdigest()


    cursor = conn.cursor(dictionary=True)
    cursor.execute('Select name, password from UserProfiles Where name=%(emp_no)s AND password=%(emp_no2)s ;',{ 'emp_no': username,'emp_no2': password })
    result=cursor.fetchall()
    conn.close()

    
    return jsonify(result)

@main.route('/flaskStatus', methods=['GET'])
def flask_status():
    return "Working Good"


# Mock Chatroom Test
# Can probably remove now.
@main.route('/chatroom_test_query', methods=['GET'])
def get_chat_messages():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
    """
        SELECT
        mock_account.name,
        mock_listing.listing_id,
        COALESCE(campaign_character_slots.campaign_listing_id, mock_listing.listing_id) as campaign_id,
        chatrooms.chatroom_id,
        chat_messages.message,
        chat_messages.timestamp

        from mock_account
        right join mock_listing on mock_account.user_id = mock_listing.creator_id
        left join campaign_character_slots on campaign_character_slots.character_listing_id = mock_listing.listing_id
        inner join chatrooms on chatrooms.campaign_id = campaign_id
        left join chat_messages on chat_messages.chatroom_id = chatrooms.chatroom_id
        where mock_account.user_id = 5
        order by chat_messages.timestamp;"""
    )

    chat_messages = cursor.fetchall()
    conn.close()
    return jsonify(chat_messages)


@main.route('/chatroom/<int:chatroom_id>', methods=['GET'])
def get_messages_from_chatroom(chatroom_id: int):
    """
        Gets all the chat messages from a specific chat room in chronological order.

        Param:
            chatroom_id: int, the id of the chatroom to get messages from

        Returns:
            str: A JSON string containing all messages from a specific chat room.
                Specifically, the following data is returned for each message:
                    user_id: of sender,
                    name: of sender,
                    message: the text,
                    timestamp: eg. "Mon, 25 Nov 2024 01:18:21 GMT":
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
    """
        SELECT
        chat_messages.user_id,
        UserProfiles.name,
        chat_messages.message,
        chat_messages.timestamp

        from chat_messages

        left join UserProfiles on UserProfiles.id = chat_messages.user_id
        where chatroom_id = %s
        order by chat_messages.timestamp;""", (chatroom_id,)
    )

    chat_messages = cursor.fetchall()
    conn.close()
    return jsonify(chat_messages)

@main.route('/chatroom/members/<int:chatroom_id>', methods=['GET'])
def get_members_of_chatroom(chatroom_id: int):
    '''Returns a JSON String of the user_id and name of all members of a chatroom.'''
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
    """
        SELECT
        mock_account.user_id,
        mock_account.name

        from mock_account
        RIGHT JOIN mock_listing on mock_account.user_id = mock_listing.creator_id
        LEFT JOIN campaign_character_slots on campaign_character_slots.character_listing_id = mock_listing.listing_id
        INNER JOIN chatrooms on chatrooms.campaign_id
            = COALESCE(campaign_character_slots.campaign_listing_id, mock_listing.listing_id)

        WHERE chatrooms.chatroom_id = %s;
       ;""", (chatroom_id,)
    )

    chatroom_members = cursor.fetchall()
    conn.close()
    return jsonify(chatroom_members)

@main.route('/send_chatroom_message', methods=["POST"])
def add_chatroom_message():
    """
        Adds a new chat message to the database.

        Params:
            ...

        Returns:
            str: ...

    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        user_id = request.form['user_id']
        chatroom_id = request.form['chatroom_id']
        message = request.form['message']

        cursor.execute(
        """
            INSERT INTO `chat_messages`(`chatroom_id`, `user_id`, `message`)
                VALUES (%s, %s, %s);
        """, (chatroom_id, user_id, message)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Chatroom message added successfully"})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@main.route('/create_chatroom', methods=["POST"])
def create_chatroom():
    """
        Creates a new chatroom given a campaign_id.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        campaign_id = request.form['campaign_id']

        cursor.execute(
        """
            INSERT INTO `chatrooms`(`campaign_id`)
                VALUES (%s);
        """, (campaign_id,)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Chatroom created successfully!"})
    
    except Exception as e:
    
        logging.error(f"Error creating chatroom: {e}")
        
        return jsonify({"error": str(e)}), 500


@main.route('/get_campaign_chatroom/<int:campaign_id>', methods=["GET"])
def campaign_chatroom_lookup(campaign_id: int):
    """
        Finds the chatroom associated with a campaign, if it exists.

        Returns:
            A JSON containing either 0 or 1 chatroom_ids associated with
            the campaign. 
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
        """
            SELECT `chatroom_id` FROM chatrooms
                WHERE `campaign_id` = %s;
        """, (campaign_id,)
        )
       
        chatroom = cursor.fetchall()
        return jsonify(chatroom)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
