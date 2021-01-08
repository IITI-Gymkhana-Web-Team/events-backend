# returns a list of commands to be executed
def get_commands(result):

    #  Example -------
    # data = {

    #     "status-1": "-1",
    #     "title-1": "Past Event 1",
    #     "description-1": "This is some text",
    #     "details-1": "This is more text for wider card Lorem Lorem Lorem Lorem",
    #     "date-1": "2021-01-08",
    #     "image-1": "https://picsum.photos/200/500",
    #     "club-1": "Web Dev Team"
    # }
    obj = {}
    for item in result:
        if '-' in item:
            [data, id] = item.split('-')
            if id not in obj:
                obj[id] = [0, 0, 0, 0, 0, 0, 0]
            if(data == 'title'):
                obj[id][0] = result['{}-{}'.format(data, id)]
            if(data == 'description'):
                obj[id][1] = result['{}-{}'.format(data, id)]
            if(data == 'details'):
                obj[id][2] = result['{}-{}'.format(data, id)]
            if(data == 'date'):
                obj[id][3] = result['{}-{}'.format(data, id)]
            if(data == 'image'):
                obj[id][4] = result['{}-{}'.format(data, id)]
            if(data == 'club'):
                obj[id][5] = result['{}-{}'.format(data, id)]
            if(data == 'status'):
                obj[id][6] = result['{}-{}'.format(data, id)]
            # if(data == 'status'):
            #     obj[id][6] = str(data[item])
    cols = ['title', 'description', 'details',
            'date_of_event', 'image', 'club', 'EVENT_STATUS']
    commands = []
    for id in obj:
        commands.append("UPDATE ALL_EVENTS SET {} = '{}', {} = '{}', {} = '{}', {} = '{}', {} = '{}', {} = '{}', {} = '{}' WHERE ID = {};".format(
            cols[0], obj[id][0], cols[1], obj[id][1], cols[2], obj[id][
                2], cols[3], obj[id][3], cols[4], obj[id][4], cols[5], obj[id][5], cols[6], obj[id][6], id
        ))

    return commands
