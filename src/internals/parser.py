from src.models.base_node import BaseNode
from src.models.node_type import NodeType
from src.models.node import Node

def identify(content: str) -> str:
  if len(content) > 2 and content[0] == '"' and content[-1] == '"':
    return NodeType.STRING
  
  nums: int = 0
  decimals: int = 0
  hyphens: int = 0

  for char in content:
    if char.isdigit():
      nums += 1
    elif char == '.':
      decimals += 1
    elif char == '-':
      hyphens += 1
    else:
      break
  else:
    if decimals > 1: return NodeType.NODE
    if hyphens > 1: return NodeType.NODE
    if hyphens == 1 and content[0] != '-': return NodeType.NODE
    if nums == 0: return NodeType.NODE
    
    return NodeType.NUMERIC

  if content.lower() in ['true', 'false']:
    return NodeType.BOOLEAN
  
  return NodeType.NODE

def convert(
  content: str,
  high_order_list: set[str]
) -> Node:
  content_type: str = identify(content)
  if content_type == NodeType.NODE:
    return Node(
      executes=content,
      high_order=content in high_order_list,
    )
  
  str_value: str | None = None
  float_value: float | None = None
  bool_value: bool | None = None

  if content_type == NodeType.STRING:
    str_value = content[1:-1]
    
  if content_type == NodeType.NUMERIC:
    float_value = float(content)
  
  if content_type == NodeType.BOOLEAN:
    bool_value = content.lower() == 'true'
  
  return Node(
    executes="base",
    value=BaseNode(
      type=content_type,
      str_value=str_value,
      float_value=float_value,
      bool_value=bool_value,
    )
  )

def parse(
  lines: list[str],
  high_order_list: set[str]
) -> Node:
  levels: list[Node] = [Node(executes="script")]
  level = [-1]

  def dive(node: Node) -> None:
    levels[-1].script = node
    levels.append(node)
    level[0] += 1

  def overtake(node: Node) -> None:
    levels[-1].next = node
    levels.pop()
    levels.append(node)

  def fly(node: Node, node_level: int) -> None:
    while node_level < level[0]:
      levels.pop()
      level[0] -= 1

    overtake(node)

  for line in lines:
    current_level: int = 0
    
    i = 0
    while i < len(line) and line[i] == ' ':
      current_level += 1
      i += 1
    
    content: str = line[i:]
    if not content:
      continue

    node: Node = convert(content, high_order_list)
    
    if current_level == level[0]:
      overtake(node)
    elif current_level > level[0]:
      dive(node)
    else:
      fly(node, current_level)

  return levels[0]

