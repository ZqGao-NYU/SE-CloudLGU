<template>
  <div>
    <!-- <el-form label="query" style="text-align: left">
    <el-input
      v-model="message"
      style="width: 220px"
      placeholder="Input Professor's name"
      prefix-icon="el-icon-search"
      clearable>
    </el-input>
    <el-button @click.native=studentCheckOT()>查询</el-button>
    </el-form> -->
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

// import axios from 'axios'
import tippy from 'tippy.js'
// import 'tippy.js/dist/tippy.css'
// import 'tippy.js/themes/light.css';
// import 'tippy.js/animations/scale.css';
import { profCheckOfficeTime, deleteOfficeTimeSlot,createOfficeTimeSlot } from '@/api/ot'
// require('@fullcalendar/core/main.min.css')
require('@fullcalendar/daygrid/main.min.css')
require('@fullcalendar/timegrid/main.min.css')

export default {
  components: {FullCalendar},
  data () {
    return {
      message: 'prof1',
      source: {
        Professor_Name: 'p1',
        success: true,
        otLists:
        [
          {
            otID: 11,
            otDate: '2022-04-10',
            otStartTime: '09:00',
            otEndTime: '10:00',
            otLocation: 'place1',
            isBooked: false,
            booked_by: ''
          },
          {
            otID: 12,
            otDate: '2022-04-11',
            otStartTime: '09:00',
            otEndTime: '10:00',
            otLocation: 'place1',
            isBooked: true,
            booked_by: 'student'
          }
        ]
      },
      calendarOptions: {
        plugins: [ DayGridPlugin, InteractionPlugin, TimeGridPlugin, ListPlugin ],
        initialView: 'timeGridWeek',
        // backgroundColor: '#D3D3D3',
        headerToolbar: { // 日历头部按钮位置
          left: 'title',
          center: '',
          right: 'prev today next'
        },
        slotLabelFormat: {
          hour: '2-digit',
          minute: '2-digit',
          meridiem: false,
          hour12: false // 设置时间为24小时
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
  created () {
    var prof_id = this.$store.state.user.token
    profCheckOfficeTime(prof_id)
    .then(res => {
      // console.log(res.data['lists'][i]['booked_byName'])
      console.log(res.data)
      if (res.data['success']){
        console.log('---ot professor: get all ot successfully---')
        this.calendarOptions.events = []
        this.message = res.data['Professor_Name']
        console.log('here')
        console.log(res.data)
        for (var i = 0; i < res.data['lists'].length; i++) {
          // console.log(res.data['lists'][i]['isbooked'])
          if (res.data['lists'][i]['isbooked']) {
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
          } else {
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

      } else{
        this.$alert("Create post fail!")
      }
    })
    .catch(function (error) { // 请求失败处理
      console.log(error);
    })
  },
  methods: {
    handleDateClick: function (arg) {
      let dateStr = arg.dateStr.substring(0, 10)
      let startStr = arg.dateStr.substring(11, 16)
      if (confirm('Do you want to create an OfficeTime at ' + dateStr + ' ' + startStr + '?')) {
        var length = prompt('Enter minutes in format like 20')
        var location = prompt('Enter the location')
        var startTime = new Date(dateStr + 'T' + startStr + ':00')
        var endTime = new Date(startTime.setMinutes(startTime.getMinutes() + parseInt(length)))
        var hours = endTime.getHours().toString()
        if (hours.length==1){hours='0'+hours}
        var minutes = endTime.getMinutes().toString()
        if (minutes.length==1){minutes='0'+minutes}
        var end = hours+':'+minutes
        var otForm={
          otDate:dateStr,
          otStartTime: startStr,
          otEndTime: end,
          otLocation: location,
          Professor_userID: this.$store.state.user.token
        }
        console.log(otForm)
  createOfficeTimeSlot(otForm)
    .then(res => {
      if (res.data['status']['success']){
        this.$message({
          message: 'Create OT Successfully',
          type: 'success'
        })
        this.$router.go(0)
      } else{
        this.$alert("Create OT fail!")
      }
    })
    .catch(function (error) { // 请求失败处理
      console.log(error);
    })

      }
    },
    handleEventClick: function (info) {
      // alert(info.event.extendedProps.Location)
      if (confirm('Do you want to delete the OfficeTime at ' + info.event.start + '?')) {
          deleteOfficeTimeSlot(info.event.id)
    .then(res => {
      if (res.data['success']){
        this.$message({
          message: 'Delete OT Successfully',
          type: 'success'
        })
        this.$router.go(0)
      } else{
        this.$alert("Delete OT fail!")
      }
    })
    .catch(function (error) { // 请求失败处理
      console.log(error);
    })
      }
    },
    handleMouseEnter: function (info) {
      if (info.event.overlap) {
        tippy(info.el, {
          content: 'Location: '+info.event.extendedProps.Location 
        })
      } else {
        tippy(info.el, {
          content: 'Location: '+info.event.extendedProps.Location + ',   booked by: ' + info.event.extendedProps.booked_by
        })
      }
    }
  }
}
</script>

<style>
</style>
