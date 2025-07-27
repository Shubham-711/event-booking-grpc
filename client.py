import grpc
import argparse

# Import the generated classes
import event_booking.event_booking_pb2 as event_booking_pb2
import event_booking.event_booking_pb2_grpc as event_booking_pb2_grpc

# Import rich for beautiful terminal output
from rich.console import Console
from rich.table import Table

def run(command, args):
    """
    Connects to the gRPC server and calls the appropriate RPC.
    """
    console = Console() # Create a console object

    # Connect to the server
    with grpc.insecure_channel('127.0.0.1:50051') as channel:
        stub = event_booking_pb2_grpc.EventBookingStub(channel)
        try:
            if command == 'create':
                request = event_booking_pb2.CreateEventRequest(name=args.name, total_tickets=args.tickets)
                response = stub.CreateEvent(request)
                console.print(f"✅ [bold green]Event Created Successfully![/bold green]")
                console.print(f"   ID: {response.id}")

            elif command == 'list':
                request = event_booking_pb2.ListEventsRequest()
                response = stub.ListEvents(request)
                if not response.events:
                    console.print("[yellow]No events found.[/yellow]")
                    return
                
                # Create a table for output
                table = Table(title="🗓️ Available Events")
                table.add_column("ID", style="cyan", no_wrap=True)
                table.add_column("Name", style="magenta")
                table.add_column("Tickets Booked", justify="right", style="green")

                for event in response.events:
                    tickets_status = f"{event.booked_tickets} / {event.total_tickets}"
                    table.add_row(event.id, event.name, tickets_status)
                
                console.print(table)

            elif command == 'book':
                request = event_booking_pb2.BookEventRequest(event_id=args.id, num_tickets=args.tickets)
                response = stub.BookEvent(request)
                console.print(f"✅ [green]Success:[/] {response.message}")

            elif command == 'cancel':
                 request = event_booking_pb2.CancelBookingRequest(event_id=args.id, num_tickets=args.tickets)
                 response = stub.CancelBooking(request)
                 console.print(f"✅ [green]Success:[/] {response.message}")
        
        except grpc.RpcError as e:
            console.print(f"❌ [bold red]An error occurred:[/] [{e.code()}] {e.details()}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='gRPC Event Booking Client')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Create command
    parser_create = subparsers.add_parser('create', help='Create a new event')
    parser_create.add_argument('--name', type=str, required=True, help='Name of the event')
    parser_create.add_argument('--tickets', type=int, required=True, help='Total number of tickets')

    # List command
    subparsers.add_parser('list', help='List all events')

    # Book command
    parser_book = subparsers.add_parser('book', help='Book tickets for an event')
    parser_book.add_argument('--id', type=str, required=True, help='Event ID')
    parser_book.add_argument('--tickets', type=int, required=True, help='Number of tickets to book')
    
    # Cancel command
    parser_cancel = subparsers.add_parser('cancel', help='Cancel a booking')
    parser_cancel.add_argument('--id', type=str, required=True, help='Event ID')
    parser_cancel.add_argument('--tickets', type=int, required=True, help='Number of tickets to cancel')

    args = parser.parse_args()
    run(args.command, args)