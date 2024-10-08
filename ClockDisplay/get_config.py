def get_config() -> list[dict]:
    config = []

    # Read configuration text file
    with open("config.cfg", 'r') as f:

        while (line := f.readline()) != '':
            if line[0] == '[':  # Add new clock

                new = {'id': int(line[7:].rstrip().removesuffix(']')), 'region': str, 'utc_offset': int}

                line = f.readline()
                new['region']     = line[line.find('=') + 1:].rstrip()

                line = f.readline()
                new['utc_offset'] = int(line[line.find('=') + 1:].rstrip())

                config.append(new)

    return config
