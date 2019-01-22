from piqueserver.commands import command
from cbc.core.twoblockcommand import two_block_command, two_block_protocol, two_block_connection
from cbc.core import cbc, buildbox


@command('box')
def box(connection, filled=""):
    connection.boxing_filled = filled.lower() == "filled"
    return two_block_command(connection,
                             'Place first corner block',
                             'Building generator cancelled')


def apply_script(protocol, connection, config):
    protocol, connection = cbc.apply_script(protocol, connection, config)

    class BoxMakerConnection(two_block_connection(connection, True)):
        second_message = 'Now break opposite corner block'
        finished_message = 'Destroying box!'

        def on_apply(self, point1, point2):
            if not self.boxing_filled:
                buildbox.build_filled(self.protocol,
                                      point1.x, point1.y, point1.z, point2.x, point2.y, point2.z,
                                      self.color, self.god, self.god_build)
            else:
                buildbox.build_empty(self.protocol,
                                     point1.x, point1.y, point1.z, point2.x, point2.y, point2.z,
                                     self.color, self.god, self.god_build)

    return two_block_protocol(protocol), BoxMakerConnection
