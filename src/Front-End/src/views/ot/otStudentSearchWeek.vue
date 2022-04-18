<template>
  <div>
    <el-form label="query" style="text-align: left;margin-left:5%;margin-top:2%;">
    <el-input
      v-model="message"
      style="width: 220px"
      placeholder="Input Faculty's name"
      prefix-icon="el-icon-search"
      clearable>
    </el-input>
    <el-button >
       <router-link :to="{name:'studentSearchProf', params:{message: message}}">Search</router-link>
    </el-button>
    <el-button style="margin-left: 56%">
        <router-link to="/officetime/student/my" > My Reservations</router-link>
    </el-button>
    </el-form>
    <p style="margin-left:35%; font-size:2rem;">Available Office Time this week</p>
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
import { searchWeek } from '@/api/ot'

// import axios from 'axios'
import tippy from 'tippy.js'
// import 'tippy.js/dist/tippy.css'
// import 'tippy.js/themes/light.css';
// import 'tippy.js/animations/scale.css';

// require('@fullcalendar/core/main.min.css')
require('@fullcalendar/daygrid/main.min.css')
require('@fullcalendar/timegrid/main.min.css')

export default {
  components: {FullCalendar},
  data () {
    return {
      message: 'prof1',
      source: {
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
            booked_by: 'student',
            prof_name: 'p3'
          },
          {
            otID: 12,
            otDate: '2022-04-11',
            otStartTime: '09:00',
            otEndTime: '10:00',
            otLocation: 'place1',
            isBooked: true,
            booked_by: 'student',
            prof_name: 'p3'
          }
        ]
      },
      calendarOptions: {
        plugins: [ DayGridPlugin, InteractionPlugin, TimeGridPlugin, ListPlugin ],
        initialView: 'dayGridWeek',
        // backgroundColor: '#D3D3D3',
        headerToolbar: { // 日历头部按钮位置
          left: 'title',
          center: '',
          right: 'prev today next'
        },
        height:660,
        slotLabelFormat: {
          hour: '2-digit',
          minute: '2-digit',
          meridiem: false,
          hour12: false // 设置时间为24小时
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
  created () {
    searchWeek()
    .then(res => {
      if (res.data['success']){
        this.$message({
          message: 'Register Successfully',
          type: 'success'
        })
      this.calendarOptions.events = []
      for (var i = 0; i < res.data['lists'].length; i++) {
        for (var j = 0; j < res.data['lists'][i]['dates'].length; i++){
        this.calendarOptions.events.push({
          id: 1,
          title: res.data['lists'][i]['profName'] + "'s Office Time",
          start: res.data['lists'][i]['dates'][j],
          allDay: true,
          overlap: true,
          extendedProps: {
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
    handleEventClick: function (info) {
      this.$router.push({
        name: 'studentSearchProf',
        params: {message: info.event.extendedProps.prof_name}
      })
    },
    // handleMouseEnter: function (info) {
    //   tippy(info.el, {
    //     content: info.event.extendedProps.Location
    //   })
    // }
  }
}
</script>

<style>
</style>
