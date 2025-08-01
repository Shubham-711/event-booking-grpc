import typer
import grpc
import event_booking.event_booking_pb2 as event_booking_pb2
import event_booking.event_booking_pb2_grpc as event_booking_pb2_grpc

app = typer.Typer()

@app.command()
def create(name: str = typer.Option(..., help="Name of the event"), 
           total_tickets: int = typer.Option(..., help="Total number of tickets available")):
    """Creates a new event."""
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = event_booking_pb2_grpc.EventBookingStub(channel)
        request = event_booking_pb2.CreateEventRequest(name=name, total_tickets=total_tickets)
        response = stub.CreateEvent(request)
        print(f"🎉 Event created successfully! ID: {response.id}")

@app.command()
def list():
    """Lists all available events."""
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = event_booking_pb2_grpc.EventBookingStub(channel)
        request = event_booking_pb2.ListEventsRequest()
        response = stub.ListEvents(request)
        if not response.events:
            print("No events found.")
            return
        print("--- Available Events ---")
        for event in response.events:
            available = event.total_tickets - event.booked_tickets
            print(f"ID: {event.id} | Name: {event.name} | Tickets Left: {available}/{event.total_tickets}")
        print("------------------------")

@app.command()
def book(event_id: str = typer.Option(..., help="The ID of the event to book"), 
         num_tickets: int = typer.Option(..., help="Number of tickets to book")):
    """Books tickets for a specific event."""
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = event_booking_pb2_grpc.EventBookingStub(channel)
        request = event_booking_pb2.BookEventRequest(event_id=event_id, num_tickets=num_tickets)
        try:
            response = stub.BookEvent(request)
            if response.success:
                print(f"✅ Success! {response.message}")
        except grpc.RpcError as e:
            print(f"❌ Error: {e.details()}")

@app.command()
def cancel(event_id: str = typer.Option(..., help="The ID of the event for which to cancel booking"), 
           num_tickets: int = typer.Option(..., help="Number of tickets to cancel")):
    """Cancels a booking for a specific event."""
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = event_booking_pb2_grpc.EventBookingStub(channel)
        request = event_booking_pb2.CancelBookingRequest(event_id=event_id, num_tickets=num_tickets)
        try:
            response = stub.CancelBooking(request)
            if response.success:
                print(f"✅ Success! {response.message}")
        except grpc.RpcError as e:
            print(f"❌ Error: {e.details()}")

if __name__ == "__main__":
    app()