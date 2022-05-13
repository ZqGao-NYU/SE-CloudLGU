<template>
  <div>
    <p style="margin-left:42%; margin-top:3%; font-size:2rem;">My Office Time</p>
    <div style="margin-left:5%; width:90%;">
      <FullCalendar
        :options="calendarOptions"
      />
    </div>
  </div>
</template>

<script>
import '@fullcalendar/core/vdom'
import FullCalendar from '@fullcalendar/vue'
import DayGridPlugin from '@fullcalendar/daygrid'
import TimeGridPlugin from '@fullcalendar/timegrid'
import InteractionPlugin from '@fullcalendar/interaction'
import ListPlugin from '@fullcalendar/list'
import tippy from 'tippy.js'
import { profCheckOfficeTime, deleteOfficeTimeSlot, createOfficeTimeSlot } from '@/api/ot'

require('@fullcalendar/daygrid/main.min.css')
require('@fullcalendar/timegrid/main.min.css')

export default {
  components: { FullCalendar },
  data() {
    return {
      message: 'prof1',
      calendarOptions: { //settings for imported fullCalendar
        plugins: [DayGridPlugin, InteractionPlugin, TimeGridPlugin, ListPlugin],
        initialView: 'timeGridWeek',
        headerToolbar: {
          left: 'title',
          center: '',
          right: 'prev today next'
        },
        slotLabelFormat: {
          hour: '2-digit',
          minute: '2-digit',
          meridiem: false,
          hour12: false
        },
        height: 660,
        customButtons: {
          addEventButton: {
            text: 'add event...',
            click: this.handleButtonClick
          }
        },
        slotDuration: '00:10:00',
        slotMaxTime: '24:00:00',
        slotMinTime: '8:00:00',
        allDaySlot: false,
        dateClick: this.handleDateClick,
        eventClick: this.handleEventClick,
        eventMouseEnter: this.handleMouseEnter,
        selectable: true,
        events: []
      }
    }
  },
  created() {
    var prof_id = this.$store.state.user.token
    //show all OT slots for professor
    profCheckOfficeTime(prof_id)
      .then(res => {
        console.log(res.data)
        if (res.data['success']) {
          console.log('---ot professor: get all ot successfully---')
          this.calendarOptions.events = []
          this.message = res.data['Professor_Name']
          console.log(res.data)
          for (var i = 0; i < res.data['lists'].length; i++) {
            if (res.data['lists'][i]['isbooked']) { // display a booked OT slot
              this.calendarOptions.events.push({
                id: res.data['lists'][i]['otID'],
                title: 'Office Time',
                start: res.data['lists'][i]['otDate'] + 'T' + res.data['lists'][i]['otStartTime'],
                end: res.data['lists'][i]['otDate'] + 'T' + res.data['lists'][i]['otEndTime'],
                overlap: false,
                extendedProps: {
                  Location: res.data['lists'][i]['otLocation'],
                  booked_by: res.data['lists'][i]['booked_byName']
                }
              })
            } else { // display an available OT slot
              this.calendarOptions.events.push({
                id: res.data['lists'][i]['otID'],
                title: 'Office Time',
                start: res.data['lists'][i]['otDate'] + 'T' + res.data['lists'][i]['otStartTime'],
                end: res.data['lists'][i]['otDate'] + 'T' + res.data['lists'][i]['otEndTime'],
                overlap: true,
                backgroundColor: '#b0e0e6',
                extendedProps: {
                  Location: res.data['lists'][i]['otLocation'],
                  booked_by: res.data['lists'][i]['booked_byName']
                }
              })
            }
          }
        } else {
          this.$alert('You do not have office time currently!')
        }
      })
      .catch(function(error) { // request failure error
        console.log(error)
      })
  },
  methods: {
     // check whether input is number
    isNumber(value) {
      if (value === '') {
        return false
      }
      const r = /^\+?[1-9][0-9]*$/
      return (r.test(value))
    },
    // click a time slot to create a new OT
    handleDateClick: function(arg) {
      const dateStr = arg.dateStr.substring(0, 10)
      const startStr = arg.dateStr.substring(11, 16)
      if (confirm('Do you want to create an OfficeTime at ' + dateStr + ' ' + startStr + '?')) {
        var length = prompt('Enter the time period in minutes')
        if (!this.isNumber(length)) {
          this.$alert('The time period must in interger form!')
          return
        } else {
          var location = prompt('Enter the location')
          // calculate the time
          var startTime = new Date(dateStr + 'T' + startStr + ':00')
          var endTime = new Date(startTime.setMinutes(startTime.getMinutes() + parseInt(length)))
          var hours = endTime.getHours().toString()
          if (hours.length == 1) { hours = '0' + hours }
          var minutes = endTime.getMinutes().toString()
          if (minutes.length == 1) { minutes = '0' + minutes }
          var end = hours + ':' + minutes
          var otForm = {
            otDate: dateStr,
            otStartTime: startStr,
            otEndTime: end,
            otLocation: location,
            Professor_userID: this.$store.state.user.token
          }
          console.log(otForm)
          // send create OT request api
          createOfficeTimeSlot(otForm)
            .then(res => {
              if (res.data['status']['success']) {
                this.$message({
                  message: 'Create OT Successfully',
                  type: 'success'
                })
                this.$router.go(0)
              } else {
                this.$alert('Create OT fail!')
              }
            })
            .catch(function(error) { // request failure error
              console.log(error)
            })
        }
      }
    },
    //click an existing event to delete
    handleEventClick: function(info) {
      if (confirm('Do you want to delete the OfficeTime at ' + info.event.start + '?')) {
        deleteOfficeTimeSlot(info.event.id)
          .then(res => {
            if (res.data['success']) {
              this.$message({
                message: 'Delete OT Successfully',
                type: 'success'
              })
              this.$router.go(0)
            } else {
              this.$alert('Delete OT fail!')
            }
          })
          .catch(function(error) { // request failure error
            console.log(error)
          })
      }
    },
    // move mouse on an event to show detail
    handleMouseEnter: function(info) {
      if (info.event.overlap) { // not be booked
        tippy(info.el, {
          content: 'Location: ' + info.event.extendedProps.Location
        })
      } else {
        tippy(info.el, { // show locatoin and booked_by
          content: 'Location: ' + info.event.extendedProps.Location + ',   booked by: ' + info.event.extendedProps.booked_by
        })
      }
    }
  }
}
</script>

<style>
</style>
