<template>
  <div>
    <el-form label="query" style="text-align: left;margin-left:5%;margin-top:2%;">
      <el-input
        v-model="message"
        style="width: 220px"
        placeholder="Input Faculty's name"
        prefix-icon="el-icon-search"
        clearable
      />
      <el-button @click.native="studentSearchProf()">Search</el-button>
      <el-button style="margin-left: 63%">
        <router-link to="/officetime/student/my">My Reservations</router-link>
      </el-button>
    </el-form>

    <div>    
      <p style="margin-left:35%; font-size:2rem;">{{ message }} Office Time</p>
      <div style="margin-left:5%; width:90%;">
        <FullCalendar :options="calendarOptions"/>
      </div>
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
import { bookOfficeTime, searchProf } from '@/api/ot'

import tippy from 'tippy.js'
require('@fullcalendar/daygrid/main.min.css')
require('@fullcalendar/timegrid/main.min.css')

export default {
  components: { FullCalendar },
  data() {
    return {
      value: '',
      message: '',
      calendarOptions: { //settings for imported fullCalendar
        plugins: [DayGridPlugin, InteractionPlugin, TimeGridPlugin, ListPlugin],
        initialView: 'timeGridWeek',
        headerToolbar: {
          left: 'title',
          center: '',
          right: 'prev today next'
        },
        height: 660,
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
    this.message = this.$route.params.message
  },
  mounted() {
    this.studentSearchProf()
  },
  methods: {
    // search professor
    studentSearchProf: function() {
      //send request to api to get data
      searchProf(this.message)
        .then(res => {
          console.log('---student get office time---')
          console.log(this.message)
          console.log(res.data)
          this.calendarOptions.events = []
          if (res.data['success']) { 
            this.$message({
              message: 'Search Successfully',
              type: 'success'
            })
            for (var i = 0; i < res.data['slots'].length; i++) {
              this.calendarOptions.events.push({
                id: res.data['slots'][i]['otID'],
                title: 'Office Time',
                start: res.data['slots'][i]['otDate'] + 'T' + res.data['slots'][i]['otStartTime'],
                end: res.data['slots'][i]['otDate'] + 'T' + res.data['slots'][i]['otEndTime'],
                backgroundColor: '#b0e0e6',
                overlap: false,
                extendedProps: {
                  Location: res.data['slots'][i]['otLocation']
                }
              })
            }
          } else {
            this.$alert('The professor does not have office time this week')
          }
        })
        .catch(function(error) { // request failure error
          console.log(error)
        })
    },
    // click an event to book OT
    handleEventClick: function(info) {
      var flag = false
      if (!info.event.overlap) {
        var hours = info.event.start.getHours().toString()
        if (hours.length == 1) { hours = '0' + hours }
        var minutes = info.event.start.getMinutes().toString()
        if (minutes.length == 1) { minutes = '0' + minutes }
        var times = hours + ':' + minutes
        if (confirm('Do you want to book the OfficeTime at ' + times + '?')) {
          var student_id = this.$store.state.user.token
          // send request to api to book OT
          bookOfficeTime(info.event.id, student_id).then(res => {
            if (res.data['success']) { //
              this.$message({
                message: 'Book Successfully',
                type: 'success'
              })
              this.studentSearchProf()
            } else {
              this.$alert('Book fail!')
            }
          }).catch(error => { // request failure error
            console.log(error)
          })
        }
      }
    },
    // move mouse on event for details
    handleMouseEnter: function(info) {
      tippy(info.el, {
        content: 'Location: ' + info.event.extendedProps.Location
      })
    }
  }
}
</script>

<style>
</style>
