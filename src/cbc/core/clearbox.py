from pyspades.contained import BlockAction
from pyspades.constants import *
from itertools import product, chain
from cbc.core import cbc, util


def clear_solid_generator(protocol, x1, y1, z1, x2, y2, z2, god=False, destroy=True):
    block_action = BlockAction()
    block_action.value = DESTROY_BLOCK
    splayer = cbc.ServerPlayer()
    block_action.player_id = splayer.player_id
    map_ = protocol.map
    check_protected = hasattr(protocol, 'protected')
    x1, x2 = sorted((x1, x2))
    y1, y2 = sorted((y1, y2))
    z1, z2 = sorted((z1, z2))
    clear_ = map_.destroy_point if destroy else map_.remove_point
    get_solid = map_.get_solid
    for x, y, z in product(range(x1, x2+1), range(y1, y2+1), range(z1, z2+1)):
        solid = get_solid(x, y, z)
        protected = (check_protected and protocol.is_protected(x, y, z))
        is_god_block = (protocol.god_blocks is not None and (x, y, z) in protocol.god_blocks)
        if not solid or (not god and (protected or is_god_block)):
            continue
        block_action.x = x
        block_action.y = y
        block_action.z = z
        protocol.send_contained(block_action, save=True)
        clear_(x, y, z)
        yield 1, 0


def clear_solid(protocol, x1, y1, z1, x2, y2, z2, god=False):
    if util.invalid_range(x1, y1, z1) or util.invalid_range(z2, y2, z2):
        raise ValueError('Invalid coordinates: ({}, {}, {}):({}, {}, {})'.format(x1, y1, z1, x2, y2, z2))
    protocol.cbc_add(clear_solid_generator(protocol, x1, y1, z1, x2, y2, z2, god))


def clear(protocol, x1, y1, z1, x2, y2, z2, god=False):
    x1, x2 = sorted((x1, x2))
    y1, y2 = sorted((y1, y2))
    z1, z2 = sorted((z1, z2))
    lst = (clear_solid_generator(protocol, x1, y1, z2, x2, y2, z2, god, False),
           clear_solid_generator(protocol, x1, y1, z1, x1, y2, z2, god, False),
           clear_solid_generator(protocol, x2, y1, z1, x2, y2, z2, god, False),
           clear_solid_generator(protocol, x1, y1, z1, x2, y1, z2, god, False),
           clear_solid_generator(protocol, x1, y2, z1, x2, y2, z2, god, False),
           clear_solid_generator(protocol, x1, y1, z1, x2, y2, z1, god, False),
           clear_solid_generator(protocol, x1, y1, z1, x2, y2, z2, god, True))
    
    protocol.cbc_add(chain.from_iterable(lst))
