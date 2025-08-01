import grpc
from concurrent import futures
import uuid
import sqlite3
import logging

import event_booking.event_booking_pb2 as event_booking_pb2
import event_booking.event_booking_pb2_grpc as event_booking_pb2_grpc

DATABASE = 'events.db'
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def init_db():
    with sqlite3.connect(DATABASE, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                total_tickets INTEGER NOT NULL,
                booked_tickets INTEGER NOT NULL
            )
        ''')
        conn.commit()

class EventBookingServicer(event_booking_pb2_grpc.EventBookingServicer):
    def __init__(self):
        init_db()

    def CreateEvent(self, request, context):
        logging.info(f"Received CreateEvent request for '{request.name}'")
        event_id = str(uuid.uuid4())
        with sqlite3.connect(DATABASE, check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO events (id, name, total_tickets, booked_tickets) VALUES (?, ?, ?, ?)",
                (event_id, request.name, request.total_tickets, 0)
            )
            conn.commit()
        logging.info(f"Event created with ID: {event_id}")
        return event_booking_pb2.Event(
            id=event_id, name=request.name, total_tickets=request.total_tickets, booked_tickets=0
        )

    def ListEvents(self, request, context):
        logging.info("Received ListEvents request.")
        events_list = []
        with sqlite3.connect(DATABASE, check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, total_tickets, booked_tickets FROM events")
            for row in cursor.fetchall():
                events_list.append(event_booking_pb2.Event(id=row[0], name=row[1], total_tickets=row[2], booked_tickets=row[3]))
        return event_booking_pb2.ListEventsResponse(events=events_list)
        
    def BookEvent(self, request, context):
        logging.info(f"Received BookEvent request for event ID: {request.event_id}")
        with sqlite3.connect(DATABASE, check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT total_tickets, booked_tickets FROM events WHERE id=?", (request.event_id,))
            row = cursor.fetchone()
            if not row:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"Event with ID '{request.event_id}' not found.")
                return event_booking_pb2.BookingResponse()
            total_tickets, booked_tickets = row
            available_tickets = total_tickets - booked_tickets
            if available_tickets < request.num_tickets:
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
                context.set_details(f"Not enough tickets available. Only {available_tickets} left.")
                return event_booking_pb2.BookingResponse()
            new_booked_tickets = booked_tickets + request.num_tickets
            cursor.execute("UPDATE events SET booked_tickets=? WHERE id=?", (new_booked_tickets, request.event_id))
            conn.commit()
        logging.info(f"Successfully booked {request.num_tickets} tickets for event {request.event_id}.")
        return event_booking_pb2.BookingResponse(success=True, message="Booking successful.")

    def CancelBooking(self, request, context):
        logging.info(f"Received CancelBooking request for event ID: {request.event_id}")
        with sqlite3.connect(DATABASE, check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT booked_tickets FROM events WHERE id=?", (request.event_id,))
            row = cursor.fetchone()
            if not row:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"Event with ID '{request.event_id}' not found.")
                return event_booking_pb2.BookingResponse()
            booked_tickets = row[0]
            if booked_tickets < request.num_tickets:
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
                context.set_details(f"Cannot cancel {request.num_tickets} tickets; only {booked_tickets} are booked.")
                return event_booking_pb2.BookingResponse()
            new_booked_tickets = booked_tickets - request.num_tickets
            cursor.execute("UPDATE events SET booked_tickets=? WHERE id=?", (new_booked_tickets, request.event_id))
            conn.commit()
        logging.info(f"Successfully cancelled {request.num_tickets} tickets for event {request.event_id}.")
        return event_booking_pb2.BookingResponse(success=True, message="Booking cancellation successful.")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    event_booking_pb2_grpc.add_EventBookingServicer_to_server(EventBookingServicer(), server)
    server.add_insecure_port('127.0.0.1:50051')
    logging.info("🚀 Server starting on port 50051 with SQLite backend...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()