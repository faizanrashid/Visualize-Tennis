from bs4 import BeautifulSoup
from bs4 import element
import json
from subprocess import Popen, PIPE

class Node(object):

	def __init__(self, name):
		self.name = name
		self.left_child = None
		self.right_child = None


def create_tree(columns, pos=1):
	#Root is the first column (starts with final)
    left = 2*pos
    right = (2*pos) - 1
    cur_stage = columns[0]
    children = [elem for elem in cur_stage.contents if type(elem) == element.Tag ]
    root = Node("")
    if len(children) >= pos-1:
        player = children[pos-1]
        name = player.find_all('p')[0].string or ""
        score = player.find_all('a')[0].string or ""
        root.name = name + " " + score
        if len(columns) > 1:
            root.left_child = create_tree(columns[1:], left)
            root.right_child = create_tree(columns[1:], right)

    return root

def return_dict_draw(root):
    ret_dict = {}
    ret_dict["name"] = root.name
    left_child = return_dict_draw(root.left_child) if root.left_child else None
    right_child = return_dict_draw(root.right_child) if root.right_child else None
    if left_child and right_child:
        children = [left_child, right_child]
        ret_dict["children"] = children

    return ret_dict


if __name__ == "__main__":
    #Fetch the data
    process = Popen(['wget', '-O', 'draw.html', 'http://www.atpworldtour.com/share/event-draws.aspx?year=2015&eventid=404&draw=ms'], 
                    stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    print "STD OUT: " + stdout + "   STD ERR: " + stderr 
    f = open("draw.html", "r")
    data = f.read()
    f.close()
    soup = BeautifulSoup(data)
    columns = soup.find_all('td')
    #Reverse the columns so the final is at the beginning
    #And get rid of the first round(not interesting enough)
    player = create_tree(columns[1:][::-1])
    f = open("draw.json", "w")
    draw_json = json.dumps(return_dict_draw(player))
    f.write(draw_json)
    f.close() 