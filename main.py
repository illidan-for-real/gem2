import datetime
import json
import ntpath
import time
import os
import math
from watchdog.observers import Observer
from watchdog.events import (FileModifiedEvent, PatternMatchingEventHandler)

observer = Observer()

# checks when file is modified
class Handler(PatternMatchingEventHandler):
    def on_modified(self, event: FileModifiedEvent):
        update_file()
        print('file modified')

saves_folder = ntpath.expandvars(r'%APPDATA%\.minecraft\saves')

if not os.path.exists('stats.txt'):
    stats_file = open('stats.txt',"w+")
    stats_file.close()

def update_file():

    saves = []

    latest_world = None

    # gets last modified world

    for i in os.listdir(saves_folder):
        full_dir = saves_folder + '\\' + i
        saves.append(i)
        last_mod = datetime.datetime.fromtimestamp(os.path.getmtime(full_dir))
        if latest_world == None:
            latest_world = [i, last_mod, full_dir]
        elif latest_world[1] < last_mod:
            latest_world = [i,last_mod, full_dir]

    stats_general = {}

    stats_custom = {}
    stats_killed = {}
    stats_mined = {}
    stats_picked_up = {}
    stats_used = {}
    stats_killed_by = {}


    # only runs if stats folder exists, useful when generating world for the first time
    if os.path.isdir(latest_world[2] + '\stats'):

        # define json stats file location & load
        stats_folder = ntpath.expandvars(latest_world[2] + '\stats')
        stats_file = open(stats_folder + '\\' + os.listdir(stats_folder)[0])
        stats = json.load(stats_file)

        # convert playtime in ticks to hours minutes and seconds (00:00:00)
        world_playtime_seconds = stats['stats']['minecraft:custom']['minecraft:play_one_minute']
        world_playtime_seconds /= 20
        ty_res = time.gmtime(world_playtime_seconds)
        world_playtime = time.strftime("%H:%M:%S",ty_res)

        # update general stats category
        stats_general.update({'world_name':latest_world[0]})
        stats_general.update({'playtime':str(world_playtime)})

        custom_dir = stats['stats']['minecraft:custom']

        total_distance = 0.0

        for i in custom_dir:

            if i == 'minecraft:killed_by':
                stats_custom.update({'killed_by':custom_dir[i]})

            if i == 'minecraft:deaths':
                stats_custom.update({'deaths':custom_dir[i]})

            if i == 'minecraft:crouch_one_cm':
                total_distance += custom_dir[i] / 100
                print(i + ' ' + str(custom_dir[i]))
            if i == 'minecraft:sprint_one_cm':
                total_distance += custom_dir[i] / 100
                print(i + ' ' + str(custom_dir[i]))
            if i == 'minecraft:walk_one_cm':
                total_distance += custom_dir[i] / 100
                print(i + ' ' + str(custom_dir[i]))
            if i == 'minecraft:walk_under_water_one_cm':
                total_distance += custom_dir[i] / 100
                print(i + ' ' + str(custom_dir[i]))
            if i == 'minecraft:walk_on_water_one_cm':
                total_distance += custom_dir[i] / 100
                print(i + ' ' + str(custom_dir[i]))
            if i == 'minecraft:swim_one_cm':
                total_distance += custom_dir[i] / 100
                print(i + ' ' + str(custom_dir[i]))
            if i == 'minecraft:fall_one_cm':
                total_distance += custom_dir[i] / 100
                print(i + ' ' + str(custom_dir[i]))
            if i == 'minecraft:fly_one_cm':
                total_distance += custom_dir[i] / 100
                print(i + ' ' + str(custom_dir[i]))

            total_distance = round(total_distance,1)

        for i in stats['stats']:

            if i == 'minecraft:custom':
                for x in stats['stats'][i]:
                    newx = x[10:]
                    newx = newx.replace("_"," ")
                    stats_custom.update({newx:stats['stats'][i][x]})

            if i == 'minecraft:killed':
                for x in stats['stats'][i]:
                    newx = x[10:]
                    newx = newx.replace("_"," ")
                    stats_killed.update({newx:stats['stats'][i][x]})

            if i == 'minecraft:mined':
                for x in stats['stats'][i]:
                    newx = x[10:]
                    newx = newx.replace("_"," ")
                    stats_mined.update({newx:stats['stats'][i][x]})

            if i == 'minecraft:picked_up':
                for x in stats['stats'][i]:
                    newx = x[10:]
                    newx = newx.replace("_"," ")
                    stats_picked_up.update({newx:stats['stats'][i][x]})

            if i == 'minecraft:used':
                for x in stats['stats'][i]:
                    newx = x[10:]
                    newx = newx.replace("_"," ")
                    stats_used.update({newx:stats['stats'][i][x]})

            if i == 'minecraft:killed_by':
                for x in stats['stats'][i]:
                    newx = x[10:]
                    newx = newx.replace("_", " ")
                    stats_killed_by.update({newx: stats['stats'][i][x]})

        # write to text file
        with open('stats.txt', 'w') as f:

            f.write('world name: ' + stats_general['world_name'] + '\n')
            f.write('playtime: ' + stats_general['playtime'] + '\n')
            f.write('\n')

            max_killed_by = [0,0]
            for i in stats_killed_by:
                if max_killed_by[1] < stats_killed_by[i]:
                    max_killed_by = [i,stats_killed_by[i]]

            for i in stats_custom:
                if i == 'deaths':
                    if stats_custom[i] < 2:
                        if max_killed_by[0] != 0:
                            f.write(str(stats_custom[i]) + ' death, ' + str(max_killed_by[0]) + ' (' + str(max_killed_by[1]) + ')' '\n')
                        else:
                            f.write(str(stats_custom[i]) + ' death' + '\n')
                    else:
                        if max_killed_by[0] != 0:
                            f.write(str(stats_custom[i]) + ' deaths, ' + str(max_killed_by[0]) + ' (' + str(max_killed_by[1]) + ')' '\n')
                        else:
                            f.write(str(stats_custom[i]) + ' deaths' + '\n')

            f.write('distance travelled: ' + str(total_distance) + 'b' + '\n')


            max_killed = [0,0]
            for i in stats_killed:
                if max_killed[1] < stats_killed[i]:
                    max_killed = [i,stats_killed[i]]
            if max_killed[1] > 0:
                f.write('most killed mob: ' + max_killed[0] + ' (' + str(max_killed[1]) + ')')
                f.write('\n' * 1)

            max_mined = [0,0]
            for i in stats_mined:
                if max_mined[1] < stats_mined[i]:
                    max_mined = [i,stats_mined[i]]
            if max_mined[1] > 0:
                f.write('most mined block: ' + max_mined[0] + ' (' + str(max_mined[1]) + ')')
                f.write('\n' * 1)

            max_used = [0,0]
            for i in stats_used:
                if max_used[1] < stats_used[i]:
                    max_used = [i,stats_used[i]]
            if max_used[1] > 0:
                f.write('most used item: ' + max_used[0] + ' (' + str(max_used[1]) + ')')
                f.write('\n' * 1)

observer.schedule(event_handler=Handler('*'), path=saves_folder)
observer.daemon = False
observer.start()