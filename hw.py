import __main__
import sys
import random, time
from datetime import date, datetime
import pandas as pd

class ScheduleManager:
    __magicianData = 'Magician.dat'
    __holidayData = 'Holidays.dat'
    __scheduleData = 'Schedule'
    __booking = 'Booking'
    __waitingSerialCache = 'waiting'
    __waitingSerial = 0
    def __init__(self):
        waitingRead = open(self.__waitingSerialCache, 'r')
        waitingSerial = waitingRead.readlines()
        waitingRead.close()
        self.__waitingSerial = int(waitingSerial[0].strip('\n'))
    def showMagician(self) -> None:
        # magicianRead = open(self.__magicianData, 'r')
        # magicians = magicianRead.readlines()
        # magicianRead.close()
        # for magician in magicians:
        #     print(magician.strip('\n'))
        magicians = pd.read_csv(self.__magicianData, sep=',')
        print(magicians)
    def addNewMagician(self, magician: str) -> None:
        magicianAppend = open(self.__magicianData, 'a')
        magicianAppend.write('\n' + magician)
    def addNewHoliday(self, holidayDate: str, holidayName: str) -> None:
        holidayAppend = open(self.__holidayData, 'a')
        holidayAppend.write('\n{},{}'.format(holidayDate, holidayName))
    def showHolidays(self) -> None:
        # holidaysRead = open(self.__holidayData, 'r')
        # holidays = holidaysRead.readlines()
        # holidaysRead.close()
        # for holiday in holidays:
        #     print(holiday.strip('\n'))
        holidays = pd.read_csv(self.__holidayData, sep=',')
        print(holidays)
    def deleteMagician(self, magicianToDelete: str) -> None:
        magicianRead = open(self.__magicianData, 'r')
        magicians = magicianRead.readlines()
        magicianRead.close()
        magicianWrite = open(self.__magicianData, 'w')
        for magician in magicians:
            if magician.strip('\n') != magicianToDelete:
                magicianWrite.write(magician)
        magicianWrite.close()
    def deleteHoliday(self, holidayDateToDelete: str) -> None:
        holidayRead = open(self.__holidayData, 'r')
        holidays = holidayRead.readlines()
        holidayRead.close()
        holidayWrite = open(self.__holidayData, 'w')
        for holiday in holidays:
            if holiday.strip('\n').split(',')[0] != holidayDateToDelete:
                holidayWrite.write(holiday)
        holidayWrite.close()
    def showBookingList(self) -> None:
        self.__showBookingList()
    def schedule(self) -> None:
        while True:
            print('''
1. Show Booking List
2. Show Current Schedule
3. Show Waiting List
4. Confirm Booking
5. Search Magicians Availability by Date
6. Put Customer in Waiting List
7. Exit

            ''')
            user_input = int(input('=> '))
            if user_input == 1:
                self.__showBookingList()
            elif user_input == 2:
                self.__showSchedule()
            elif user_input == 3:
                self.__showWaitingList()
            elif user_input == 4:
                date = str(input('Enter the Holidays Date: '))
                magician = str(input('Enter the Magician Name to assign: '))
                customer = str(input('Enter the Customer Name: '))
                self.__confirmBooking(date, magician, customer)
            elif user_input == 5:
                date = str(input('Enter the Holiday Date: '))
                self.__searchMagicians(date)
            elif user_input == 6:
                customer = str(input('Enter the Customer Name: '))
                date = str(input('Enter Holiday Date: '))
                self.__customerToWaitingList(customer, date)                                           
            elif user_input == 7:
                break
    
    def __showBookingList(self) -> None:
        bookings = pd.read_csv(self.__booking, sep=',')
        print(bookings)
    def __showSchedule(self) -> None:
        schedule = pd.read_csv(self.__scheduleData, sep=',')
        print(schedule)
    def __showWaitingList(self) -> None:
        bookingRead = open(self.__booking, 'r')
        bookings = bookingRead.readlines()
        bookingRead.close()
        for booking in bookings:
            status = booking.strip('\n').split(',')[2]
            if status.__contains__('Waiting No'):
                print(booking.strip('\n'))
    def __confirmBooking(self, date: str, magician: str, customer: str) -> None:
        exitCode = 0
        scheduleRead = open(self.__scheduleData, 'r')
        schedules = scheduleRead.readlines()
        scheduleRead.close()
        for schedule in schedules:
            s_magician = schedule.strip('\n').split(',')[0]
            s_date = schedule.strip('\n').split(',')[1]    
            if s_magician ==  magician and s_date == date:
                print('Magician {} already have a booking on {}. Try another Magician or date'.format(s_magician, s_date))
                exitCode = 1
        if exitCode == 0:
            scheduleAppend = open(self.__scheduleData, 'a')
            scheduleAppend.write('\n{},{},{}'.format(magician, date, customer))

            bookingRead = open(self.__booking, 'r')
            bookings = bookingRead.readlines()
            bookingRead.close()
            bookingWrite = open(self.__booking, 'w')
            for booking in bookings:
                b_customer = booking.strip('\n').split(',')[0]
                b_date = booking.strip('\n').split(',')[1]
                if b_customer == customer and b_date == date:
                    bookingWrite.write('{},{},Booking Confirmed'.format(b_customer, b_date))
                    bookingWrite.write('\n')
                else:
                    bookingWrite.write(booking)
            bookingWrite.close()        
    def __searchMagicians(self, date: str) -> None:
        busyMagician = []
        magicianRead = open(self.__magicianData, 'r')
        magicians = magicianRead.readlines()
        magicianRead.close()
        scheduleRead = open(self.__scheduleData, 'r')
        schedules = scheduleRead.readlines()
        scheduleRead.close()
        for schedule in schedules:
            s = schedule.strip('\n')
            s_magician = s.split(',')[0]
            s_date = s.split(',')[1]
            if s_date == date:
                busyMagician.append(s_magician)
        for magician in magicians:
            if magician.strip('\n') not in busyMagician:
                print(magician.strip('\n'))

    def __customerToWaitingList(self, customer: str, date: str) -> None:
        bookingRead = open(self.__booking, 'r')
        bookings = bookingRead.readlines()
        bookingRead.close()
        bookingWrite = open(self.__booking, 'w')
        waitingWrite = open(self.__waitingSerialCache, 'w')
        for booking in bookings:
            b_customer = booking.strip('\n').split(',')[0]
            b_date = booking.strip('\n').split(',')[1]
            if b_customer == customer and b_date == date:
                self.__waitingSerial += 1
                print(self.__waitingSerial)
                bookingWrite.write('{},{},Waiting No:{}'.format(b_customer, b_date, str(self.__waitingSerial).zfill(5)))
                bookingWrite.write('\n')
            else:
                bookingWrite.write(booking)
        bookingWrite.close()
        waitingWrite.write(str(self.__waitingSerial))
        waitingWrite.close()
    def status(self) -> None:
        self.__showSchedule()
    def cancel(self):
        while True:
            print('''
1. Show Active Schedule
2. Delete Reservation
3. Show Waiting List
4. Exit

            ''')
            user_input = int(input('=> '))
            if user_input == 1:
                self.__showSchedule()
            elif user_input == 2:
                magician = str(input('Enter the Magicians Name: '))
                date = str(input('Enter the Date: '))
                self.__deleteReservation(magician, date)
            elif user_input == 3:
                self.__showWaitingList()
            elif user_input == 4:
                break
    def __deleteReservation(self, magician: str, date: str) -> None:
        waitingOrder = {}
        scheduleRead = open(self.__scheduleData, 'r')
        schedules = scheduleRead.readlines()
        scheduleRead.close()
        scheduleWrite = open(self.__scheduleData, 'w')
        for schedule in schedules:
            s = schedule.strip('\n')
            s_magician = s.split(',')[0]
            s_date = s.split(',')[1]
            if s_magician != magician and s_date != date:
                scheduleWrite.write(schedule)
        bookingRead = open(self.__booking, 'r')
        bookings = bookingRead.readlines()
        bookingRead.close()
        for booking in bookings:
            b_customer = booking.strip('\n').split(',')[0]
            b_date = booking.strip('\n').split(',')[1]
            b_status = booking.strip('\n').split(',')[2]
            if b_date == date and b_status.__contains__('Waiting No'):
                waitingOrder[int(b_status.split(':')[1])] = b_customer
        topWaiting = min(waitingOrder.keys())
        w_customer = waitingOrder[topWaiting]
        scheduleWrite.write('{},{},{}'.format(magician, date, w_customer))
        scheduleWrite.write('\n')
        scheduleWrite.close()
        bookingWrite = open(self.__booking, 'w')
        for booking in bookings:
            b_customer = booking.strip('\n').split(',')[0]
            b_date = booking.strip('\n').split(',')[1]
            b_status = booking.strip('\n').split(',')[2]
            if b_customer == w_customer and b_date == date and b_status.__contains__('Waiting No'):
                bookingWrite.write('{},{},{}'.format(b_customer, b_date, 'Booking Confirmed'))
                bookingWrite.write('\n')
            else:
                bookingWrite.write(booking)

def main():
    sch = ScheduleManager()
    while True:
        print('''
1. Show All Magicians
2. Add New Magician
3. Delete Magician
4. Show All Holidays
5. Add New Holidays
6. Delete Holiday
7. Show Booking Info
8. Schedule
9. Cancel
10. Status
11. Exit/Quit

        ''')
        user_input = int(input('=> '))
        if user_input == 1:
            sch.showMagician() 
        elif user_input == 2:
            newMagician = str(input('Enter New Magicians Name: '))
            sch.addNewMagician(newMagician)
        elif user_input == 3:
            deletingMagician = str(input('Enter the Magician Name to Delete: '))
            sch.deleteMagician(deletingMagician)
        elif user_input == 4:
            sch.showHolidays()        
        elif user_input == 5:
            newHolidayDate = str(input('Enter New Holidays Date(format: Jun 1 2021): '))
            newHolidayName = str(input('Enter New Holidays Name: '))
            sch.addNewHoliday(newHolidayDate, newHolidayName)           
        elif user_input == 6:
            deletingHoliday = str(input('Enter Holiday Date to Delete (format: Jun 1 2021): '))
            sch.deleteHoliday(deletingHoliday)
        elif user_input == 7:
            sch.showBookingList()
        elif user_input == 8:
            sch.schedule()
        elif user_input == 9:
            sch.cancel()  
        elif user_input == 10:
            sch.status()
        elif user_input == 11:
            sys.exit(0)

if __name__ == '__main__':
    main()