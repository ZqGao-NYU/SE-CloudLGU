<template>
  <div>
    <el-form label="query" style="text-align: left; margin-left:5%;margin-top:2%;">
      <el-input
        v-model="message"
        style="width: 220px"
        placeholder="Input Faculty's name"
        prefix-icon="el-icon-search"
        clearable
      />
      <el-button>
        <router-link :to="{name:'studentSearchProf', params:{message: message}}"> Search</router-link>
      </el-button>
      <el-button style="margin-left:63%">
        <router-link to="/officetime/student/my"> My Reservations</router-link>
      </el-button>
    </el-form>
    <p style="margin-left:40%; font-size:2rem;">My Booked Office Time</p>
    <div style="margin-left:5%; width:90%;">
    <FullCalendar:options="calendarOptions"/>
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
import { studentCheckOfficeTime } from '@/api/ot'
import tippy from 'tippy.js'
require('@fullcalendar/daygrid/main.min.css')
require('@fullcalendar/timegrid/main.min.css')

export default {
  components: { FullCalendar },
  data() {
    return {
      message: '',
      calendarOptions: { //settings for imported fullCalendar
        plugins: [DayGridPlugin, InteractionPlugin, TimeGridPlugin, ListPlugin],
        initialView: 'timeGridWeek',
        height: 660,
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
        selectable: false,
        events: []
      }
    }
  },
  created() {
    var id = this.$store.state.user.token
    // show OT reservation information for student
    studentCheckOfficeTime(id)
      .then(res => {
        if (res.data['success']) {
          this.calendarOptions.events = []
          for (var i = 0; i < res.data['lists'].length; i++) {
            this.calendarOptions.events.push({
              id: res.data['lists'][i]['otID'].toString(),
              title: res.data['lists'][i]['prof_name'] + "'s Office Time",
              start: res.data['lists'][i]['otDate'] + 'T' + res.data['lists'][i]['otStartTime'],
              end: res.data['lists'][i]['otDate'] + 'T' + res.data['lists'][i]['otEndTime'],
              overlap: true,
              extendedProps: {
                Location: res.data['lists'][i]['otLocation']
              }
            })
          }
        } else {
          this.$alert('You do not have any reservation currently!')
        }
      })
      .catch(function(error) { // request failure error
        console.log(error)
      })
  },
  methods: {
    handleMouseEnter: function(info) {
      // alert('Event: ' + info.event.title)
      tippy(info.el, {
        content: 'Location: ' + info.event.extendedProps.Location
      })
    }
  }
}
</script>

<style>
</style>
