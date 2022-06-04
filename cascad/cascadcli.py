import argparse
from cascad.agents import create_agent


def process(args):
    if args.subparser == 'agent':
        if args.create:
            create_agent(args.agent_name, args.target_path)
            pass
        pass

def init_parser(parser: argparse.ArgumentParser): 
    subparsers = parser.add_subparsers(dest='subparser')

    parser_agent = subparsers.add_parser('agent')
    parser_agent.add_argument(
        '-c', '--create', dest='create', default=False, help='create an agent', action='store_true'
    )
    parser_agent.add_argument(
        '-n', '--name', dest='agent_name', default='zlagent', help='the name of agent to create'
    )
    parser_agent.add_argument(
        '-p', '--path', dest='target_path', default='', help='the target path of created agent'
    )

    
    parser_server = subparsers.add_parser('server')
    parser_server.add_argument(
        '-s', '--start', dest='start', default=False, help='start the server', action='store_true'
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    init_parser(parser)
    args = parser.parse_args()
    process(args)
    