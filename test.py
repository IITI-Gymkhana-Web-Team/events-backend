# returns a list of commands to be executed
def get_commands(data, table_name):

    x = data
    #  Example -------
    # {
    #     "32": ["title", "description", "details", "20-11-10", "image_url", "club-name"],
    #     "12": ["title", "description", "details", "20-11-10", "image_url", "club-name"]
    # }
    obj = {}
    for item in x:
        if '-' in item:
            [data, id] = item.split('-')
            if id not in obj:
                obj[id] = [0, 0, 0, 0, 0, 0]
            if(data == 'title'):
                obj[id][0] = x[item]
            if(data == 'description'):
                obj[id][1] = x[item]
            if(data == 'details'):
                obj[id][2] = x[item]
            if(data == 'date'):
                obj[id][3] = x[item]
            if(data == 'image'):
                obj[id][4] = x[item]
            if(data == 'club'):
                obj[id][5] = x[item]
            # print("UPDATE TABLE SET {} = '{}' WHERE ID = {};".format(data,x[item], id))
    cols = ['title', 'description', 'details',
            'date_of_event', 'image', 'club']
    commands = []
    for id in obj:
        commands.append("UPDATE {} SET {} = '{}', {} = '{}', {} = '{}', {} = '{}', {} = '{}', {} = '{}' WHERE ID = {};".format(
            table_name, cols[0], obj[id][0], cols[1], obj[id][1], cols[2], obj[id][
                2], cols[3], obj[id][3], cols[4], obj[id][4], cols[5], obj[id][5], id
        ))

    return commands

    # print(obj)
