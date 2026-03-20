#  - 0xf -> 0x100000002 -> 0x1
# - 0xd -> 0x100000002 -> 0x1
# - 0xb -> 0x400000009 -> 0x4
# - 0x9 -> 0x200000005 -> 0x2
# - 0x7 -> 0x40000000b -> 0x4
# - 0x5 -> 0x30000000a -> 0x3
# - 0x3 -> 0x100000005 -> 0x1
dic = {
    0xf: 1,
    0xd: 1,
    0xb: 4,
    0x9: 2,
    0x7: 4,
    0x5: 3,
    0x3: 1
}


class Node:
    def __init__(self, idx, parent_idx, pos, sz):
        self.ch = [None] * sz # children of the current node
        self.idx = idx
        self.parent = parent_idx
        self.pos = pos

# root does not appear in the compression data
class Data:
    def __init__(self, nodes, comp, node_num):
        self.nodes = nodes
        self.comp = comp
        self.node_num = node_num
    
def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]

def parse(f):
    f = f[4:] # ignore COMP str
    node_num = f[0]
    f = f[1:]
    node_count = (node_num + 253) // (node_num - 1) + 256
    print(f"Node num: {node_num} Node count: {node_count}")

    tree_data = f[:(node_count - 1) * 3] # ignore root 
    comp = f[(node_count-1) * 3:] # compressed data
    # comp = f[-1]
    if type(comp) == int: comp = int.to_bytes(comp)
    nodes = []

    for i in range(0, len(tree_data), 3):
        x = tree_data[i:i+3]
        parent = int.from_bytes(x[:2][::-1],byteorder='big') - 1
        pos = x[-1]
        # print("Parent: ", parent, pos)
        n = Node(i // 3, parent, pos, node_num)
        print(i//3, x.hex(), hex(parent))
        nodes.append(n)
    last_node = Node(nodes[-1].parent, None, 0, node_num) # root node
    nodes.append(last_node)
    # print(f"Parsed: {len(nodes)}, {comp}, {node_num}")
    ret = Data(nodes, comp, node_num)
    return ret

def make_tree(nodes):
    for i,v in enumerate(nodes):
        if i == len(nodes)-1: break
        pidx = v.parent
        pos = v.pos
        pnode = nodes[pidx]
        pnode.ch[pos] = v

def search(nodes, path):
    print("path: ", path[:100])
    root = nodes[-1]
    cur = root
    ret = []
    # print(cur)
    for i in path:

        # print("Searching: ", i, cur, cur.ch)
        
        if cur == None:
            print("failed", i)
            input()
            cur = root
            continue
        while (cur.ch[i] == None):
            cur = cur.ch[0] 
        # if cur.idx == 0xca: 
        #     input()
        cur = cur.ch[i] 

        # print("search val: ", i, hex(cur.idx))
        if cur.idx <= 255:
            # input()
            # ret += chr(cur.idx)
            ret.append(cur.idx)
            cur = root
    return ret[::-1]

def decompress(d):
    # Convert number to base n
    comp = d.comp
    nodes = d.nodes
    node_num = d.node_num
    ret = []
    to_iter = []
    max_len = 0
    for i in range(0, len(comp), dic[node_num]):
        x = comp[i:i+ dic[node_num]]
        y = numberToBase(int.from_bytes(x, byteorder='little'), node_num)
        if max_len < len(y):
            max_len = len(y)
        if len(y) < max_len:
            y = [0] * (max_len - len(y)) + y
        to_iter+=y

    z = search(nodes, to_iter)
    # print(z)
    ret = z[::-1]
        # ret += (z[::-1])
    return  ret

def main():

    # f = open('./AA.comp', 'rb').read()
    f = open('./A.comp', 'rb').read()
    # f = open('./ilovetrees.jpg.comp.comp.comp.comp.comp', 'rb').read()
    d = parse(f)
    comp = d.comp
    nodes = d.nodes
    node_num = d.node_num
    print(len(nodes))
    # print("Comp: ", comp.hex())
    print("check: ", nodes[-1].idx, nodes[-1].parent)
    print("check 2: ", nodes[-2].idx, nodes[-2].parent)


    make_tree(nodes)
    print(nodes[-1].ch)
    val = decompress(d)
    # print("val: ", val)
    # print(val)
    f2 = open('./decomp', 'wb')
    for i in val: 
        # print("val: ", hex(i))
        try:
            f2.write(int.to_bytes(i))
        except: 
            print(i)
            input()
    f2.close()
    print("Done writing")
    

if __name__ == '__main__':
    main()
    # flag: DH{66025bb8470e0c39e898c6f8e4560aedca0c24f240d9ed9f7ddd5a7233a6cfee}
