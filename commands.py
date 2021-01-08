# returns a list of commands to be executed
def get_commands(data):

    print('hlo from test')
    print(data)
    #  Example -------
    # {
    #
    #    "status-1":"-1",
    #    "title-1":"Past Event 1",
    #    "description-1":"This is some text",
    #    "details-1":"This is more text for wider card Lorem Lorem Lorem Lorem",
    #    "date-1":"2021-01-08",
    #    "image-1":"https://picsum.photos/200/500",
    #    "club-1":"Web Dev Team"
    # }
    obj = {}
    for item in data:
        if '-' in item:
            [data, id] = item.split('-')
            if id not in obj:
                obj[id] = [0, 0, 0, 0, 0, 0, 0]
            if(data == 'title'):
                obj[id][0] = data[item]
            if(data == 'description'):
                obj[id][1] = data[item]
            if(data == 'details'):
                obj[id][2] = data[item]
            if(data == 'date'):
                obj[id][3] = data[item]
            if(data == 'image'):
                obj[id][4] = data[item]
            if(data == 'club'):
                obj[id][5] = data[item]
            if(data == 'status'):
                obj[id][6] = data[item]
            print("UPDATE TABLE SET {} = '{}' WHERE ID = {};".format(
                data, data[item], id))
    # cols = ['title', 'description', 'details',
    #         'date_of_event', 'image', 'club']
    # commands = []
    # for id in obj:
    #     commands.append("UPDATE {} SET {} = '{}', {} = '{}', {} = '{}', {} = '{}', {} = '{}', {} = '{}' WHERE ID = {};".format(
    #         table_name, cols[0], obj[id][0], cols[1], obj[id][1], cols[2], obj[id][
    #             2], cols[3], obj[id][3], cols[4], obj[id][4], cols[5], obj[id][5], id
    #     ))

    # return commands

    # print(obj)
