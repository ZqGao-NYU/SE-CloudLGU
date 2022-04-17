<template>
  <div class="user">
    <div class="user_table" style="width: 63%;">
        <el-table
        :data="tableDataShow.slice((curPage-1)*pagesize,curPage*pagesize)"
        :header-cell-style="{color:'#000000'}"
        stripe>
        <el-table-column
            label="UserName"
            prop="Username"
            width="150%">
          <template slot-scope="scope">
            <span style="color:#000000">{{ scope.row.Username }}</span>
          </template>
        </el-table-column>

        <el-table-column
            label="Role"
            prop="Role"
            width="100%">
          <template slot-scope="scope">
            <span style="color:#000000">{{ scope.row.Role }}</span>
          </template>
        </el-table-column>

        <el-table-column
            label="Email"
            prop="Email"
            width="240%">
          <template slot-scope="scope">
            <span style="color:#000000">{{ scope.row.Email }}</span>
          </template>
        </el-table-column>

        <el-table-column
            label="Password"
            prop="Password"
            width="170%">
          <template slot-scope="scope">
            <span style="color:#000000">{{ scope.row.Password }}</span>
          </template>
        </el-table-column>

        <el-table-column
            label="Intro"
            prop="Intro"
            width="200%">
          <template slot-scope="scope">
            <span style="color:#000000">{{ scope.row.Intro }}</span>
          </template>
        </el-table-column>

        <el-table-column
            label=""
            width="100%"
            align="left"
        >
          <template slot-scope="scope">
            <el-dropdown>
              <div class = "icon-setting">
              <i class="el-icon-s-tools"></i>
              <span class="el-dropdown-link">
                <i class="el-icon-arrow-down el-icon--right"></i>
              </span>
              <el-dropdown-menu>
                <el-dropdown-item style="color:#000000" disabled>Setting</el-dropdown-item>
                <v-divider></v-divider>
                <el-dropdown-item style="color:#000000" @click.native="editCommand(scope.$index)">Edit</el-dropdown-item>
                <el-dropdown-item style="color:#FA0000" @click.native="deleteCommand(scope.$index)">Delete</el-dropdown-item>
              </el-dropdown-menu>
              </div>
            </el-dropdown>
          </template>
        </el-table-column>
        </el-table>
    </div>
    <div class="title">
      <h1>Admin Area&nbsp;>&nbsp;Manage Users</h1>
    </div>
    <div class="search">
      <el-input
        placeholder="Search by name, role or email"
        prefix-icon="el-icon-search"
        v-model="input_search">
      </el-input>
      <v-divider></v-divider>
    </div>
    <div class="search_button">
      <v-btn color="#50A75E" class = "submit white--text" @click="doFilter" height="30" > Search </v-btn>
    </div>
    <div class="sort-title">
      <h2>Sort by</h2>
    </div>
    <div class="sort">
      <el-select v-model="value" placeholder="..."
        @change="selectTrigger">
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value">
        </el-option>
      </el-select>
      <v-divider></v-divider>
    </div>
    <div class="edit_dialog">
      <el-dialog
        title="Edit User Information"
        :visible.sync="editdialogVisible"
        width="50%"
        style="font-family: Lucida Sans; color:#000000"
        append-to-body>
          <el-form label-width="100px" :model="edit_user" :rules="edit_rules" ref="edit_user">
            <el-form-item label="Username" prop="username">
            <el-input v-model="edit_user.username" placeholder=""></el-input>
            </el-form-item>
            <el-form-item label="Role" prop="role">
              <el-radio-group v-model="edit_user.role_radio" style="width:100%">
              <el-radio :label="0">Admin</el-radio>
              <el-radio :label="1">Faculty</el-radio>
              <el-radio :label="2">Student</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="Email" prop="email" >
            <el-input v-model="edit_user.email" placeholder="" :disabled="true"></el-input>
            </el-form-item>
            <el-form-item label="Password" prop="password">
            <el-input v-model="edit_user.password" placeholder=""></el-input>
            </el-form-item>
            <el-form-item label="Intro" prop="intro">
            <el-input v-model="edit_user.intro" placeholder=""></el-input>
            </el-form-item>
            <el-form-item el-form-item>
              <v-btn color="#FBE87985" class = "cancel#AAAAAA--text" @click="cancelEdit" height="30" >Cancel</v-btn>
              <v-btn color="#50A75E" class = "submit white--text" @click="editUser('edit_user')" height="30" style="margin-left:20px;">Submit</v-btn>
            </el-form-item>
          </el-form>
      </el-dialog>
    </div>
    <div class="table_pagination">
      <el-pagination
        :current-page.sync="curPage"
        :page-size="pagesize"
        :pager-count="7"
        :total="tableDataShow.length"
        background
        layout="prev, pager, next">
      </el-pagination>
    </div>
    <div class="delete_hint">
    <el-dialog
      title=""
      :visible.sync="deletedialogVisible"
      width="35%"
      style="font-family: Lucida Sans; color:#000000"
      append-to-body>
        <span>Confirm to delete the user?</span>
        <span slot="footer" class="dialog-footer">
        <v-btn color="#FBE87985" class = "cancel#AAAAAA--text" @click="cancelDelete" height="30" >Cancel</v-btn>
        <v-btn color="#50A75E" class = "submit white--text" @click="deleteUser" height="30" style="margin-left:20px;">Confirm</v-btn>
        </span>
    </el-dialog>
    </div>
    <div class="edit-dialog-true">
      <el-dialog
      title="Tooltip"
      :visible.sync="dialogVisibleTrue"
      width="30%"
      style="color:#000000"
      append-to-body>
      <span>The user has been edited!</span>
      <span slot="footer" class="dialog-footer">
      <v-btn color="#50A75E" class = "submit white--text" @click="setFlag" height="30" style="margin-left:80px;">Done</v-btn>
      </span>
      </el-dialog>
    </div>
    <div class="edit-dialog-false">
      <el-dialog
      title="Tooltip"
      :visible.sync="dialogVisibleFalse"
      width="20%"
      style="color:#000000"
      append-to-body>
      <span>The username is used! <br/> Please choose another username.</span>
      <span slot="footer" class="dialog-footer">
      <v-btn color="#50A75E" class = "submit white--text" @click="setFlag" height="30" style="margin-left:80px;">Done</v-btn>
      </span>
      </el-dialog>
    </div>
  </div>

</template>

<script>

export default {
  name: 'ChangePassword',
  data () {
    return {
      input_search: '',
      tableData: [],
      tableDataShow: [],
      options: [{
        value: 'option1',
        label: 'UserName'
      },
      {
        value: 'option2',
        label: 'Role'
      },
      {
        value: 'option3',
        label: 'Email'
      }],
      value: '',
      edit_user: {
        username: '',
        role_radio: 0,
        email: '',
        password: '',
        intro: ''
      },
      roles: ['admin', 'faculty', 'student'],
      user_role: { 0: 'Student', 1: 'Teacher', 2: 'Administrator' },
      edit_rules: {
        username: [{
          min: 5,
          max: 12,
          message: 'Range within 5 to 12 characters',
          trigger: 'blur'
          }],
        password: [
          {
            required: true,
            message: 'Password cannot be empty',
            trigger: 'blur'
          },
          {
            min: 6,
            max: 12,
            message: 'Range within 6 to 12 characters',
            trigger: 'blur'
          }
        ],
        intro: [{
          min: 0,
          max: 40,
          message: 'maximum 40 characters',
          trigger: 'blur'
        }]
      },
      deletedialogVisible: false,
      editdialogVisible: false,
      dialogVisibleFalse: false,
      dialogVisibleTrue: false,
      edit_index: 0,
      delete_index: 0,
      curPage: 1,
      pagesize: 6
    }
  },
  created (){
    this.getMockUsersData()
  },
  mounted () {
    this.getUsersData()
  },
  methods: {
    getUsersData () {
      this.tableData = this.tableDataShow
      console.log(this.tableDataShow);
    },

    getMockUsersData () {
      this.tableDataShow = [
        {
          Username: 'admin1',
          Role: 'admin',
          Email: 'admin@cuhk.edu.cn',
          Password: '123456',
          Intro: 'I am a super admin'
        },
        {
          Username: 'admin2',
          Role: 'admin',
          Email: 'adminTest@cuhk.edu.cn',
          Password: '123456aaaa',
          Intro: 'I am an admin'
        },
        {
          Username: 'faculty',
          Role: 'faculty',
          Email: 'faculty@cuhk.edu.cn',
          Password: '123456',
          Intro: 'I am a faculty'
        },
        {
          Username: 'Amy',
          Role: 'student',
          Email: '119000000@link.cuhk.edu.cn',
          Password: 'aaaaaa',
          Intro: 'I am a student'
        },
        {
          Username: 'Bob',
          Role: 'student',
          Email: '119000001@link.cuhk.edu.cn',
          Password: 'aaaaaa',
          Intro: 'I am a student'
        },
        {
          Username: 'Cissy',
          Role: 'student',
          Email: '119000002@link.cuhk.edu.cn',
          Password: 'aaaaaa',
          Intro: 'I am a student'
        },
        {
          Username: 'Daniel',
          Role: 'student',
          Email: '119000003@link.cuhk.edu.cn',
          Password: 'aaaaaa',
          Intro: 'I am a student'
        },
        {
          Username: 'Emily',
          Role: 'student',
          Email: '119000004@link.cuhk.edu.cn',
          Password: 'aaaaaa',
          Intro: 'I am a student'
        },
        {
          Username: 'Fred',
          Role: 'student',
          Email: '119000005@link.cuhk.edu.cn',
          Password: 'aaaaaa',
          Intro: 'I am a student'
        },
      ]

    
    },

    doFilter () {
      if (this.input_search === '') {
        this.tableDataShow = this.tableData
        return
      }
      this.tableDataShow = []
      var temp_search = this.input_search.toLowerCase()
      this.tableData.forEach((value, index) => {
        if (value.Username) {
          if (value.Username.toLowerCase().indexOf(temp_search) >= 0) {
            this.tableDataShow.push(value)
          } else if (value.Role.toLowerCase().indexOf(temp_search) >= 0) {
            this.tableDataShow.push(value)
          } else if (value.Email.toLowerCase().indexOf(temp_search) >= 0) {
            this.tableDataShow.push(value)
          }
        }
      })
      this.curPage = 1
    },

    selectTrigger (value) {
      if (value === 'option1') {
        this.sortByKey(this.tableDataShow, 'Username')
      }
      if (value === 'option2') {
        this.sortByKey(this.tableDataShow, 'Role')
      }
      if (value === 'option3') {
        this.sortByKey(this.tableDataShow, 'Email')
      }
    },

    editCommand (index) {
      this.editdialogVisible = true
      this.edit_index = index
      index = (this.curPage - 1) * this.pagesize + index
      this.edit_user.username = this.tableDataShow[index].Username
      this.edit_user.role_radio = this.roles.indexOf(this.tableDataShow[index].Role)
      this.edit_user.email = this.tableDataShow[index].Email
      this.edit_user.password = this.tableDataShow[index].Password
      this.edit_user.intro = this.tableDataShow[index].Intro
    },

    deleteCommand (index) {
      this.deletedialogVisible = true
      this.delete_index = index
    },

    editUser (formName) {
      // eslint-disable-next-line camelcase
      var new_index = this.edit_index + (this.curPage - 1) * this.pagesize
      this.$refs[formName].validate((valid) => {
        if (valid) {/*
          var params = {
            // id: this.tableDataShow[new_index].ID,
            username: this.edit_user.username,
            role: this.roles[this.edit_user.role_radio], // 0: Admin 1: Staff Level1 2: Staff Level2 3: Staff Level3 4: Staff Level4 5: Teacher 6:Student
            email: this.edit_user.email,
            password: this.edit_user.password
            intro: this.edit_user.intro
          }
          this.$axios.request({
            url: '/django_api/admin_edit_user/',
            method: 'post',
            headers: {
              'Content-type': 'application/json'
            },
            data: params
          })
            .then(res => {
              if (res.data.status === 1) {
                this.dialogVisibleTrue = true
              } else if (res.data.status === 0) {
                this.dialogVisibleFalse = true
              }
            })*/
          this.tableDataShow[new_index].Username = this.edit_user.username,
          this.tableDataShow[new_index].Role = this.roles[this.edit_user.role_radio],
          this.tableDataShow[new_index].Email = this.edit_user.email,
          this.tableDataShow[new_index].Password = this.edit_user.password,
          this.tableDataShow[new_index].Intro = this.edit_user.intro
        }
        this.edit_user.username = ''
        this.edit_user.role_radio = 0
        this.edit_user.password = ''
        this.edit_user.email = ''
        this.edit_user.intro = ''
        this.editdialogVisible = false
        this.getUsersData()
      })
    },
    deleteUser () {
      // eslint-disable-next-line camelcase
      var new_index = this.delete_index + (this.curPage - 1) * this.pagesize
      /*var params = {
        id: this.tableDataShow[new_index].ID
      }
      this.$axios.get('/django_api/admin_delete_user/?' + this.$qs.stringify(params))
        .then(res => {
          this.deletedialogVisible = false
          this.getUsersData()
        })*/
      this.tableDataShow.splice(new_index, 1)
      this.deletedialogVisible = false
      this.getUsersData()
    },
    cancelEdit () {
      this.edit_user.username = ''
      this.edit_user.role_radio = 0
      this.edit_user.password = ''
      this.edit_user.email = ''
      this.edit_user.intro = ''
      this.editdialogVisible = false
    },
    cancelDelete () {
      this.deletedialogVisible = false
    },
    setFlag () {
      this.dialogVisibleTrue = false
      this.dialogVisibleFalse = false
    },
    sortByKey (array, key) {
      return array.sort(function (a, b) {
        var x = a[key]
        var y = b[key]
        return ((x < y) ? -1 : ((x < y) ? 1 : 0))
      })
    }
  }
}
</script>

<style>
.user {
  overflow-y: auto;
}

.user .privilege-navigator {
  position: relative;
  margin-top: 3%;
  margin-left: 3%;
}

.user .user_table {
  position: absolute;
  left: 24%;
  top: 25%;
  width: 63%;
}

.user .user_table .icon-setting {
  font-size:20px;
}

.user .create-user {
  position: absolute;
  left: 80%;
  top: 6%;
}

.user .title {
  position: absolute;
  left: 21.5%;
  top: 6%;
  width: 25%;
}

.user .title h1{
  position: absolute;
  font-size: 18px;
  font-weight: bold;
  font-family: "Lucida Sans", "Lucida Sans Regular", "Lucida Grande",
  "Lucida Sans Unicode", Geneva, Verdana, sans-serif;
  color: #000000;
}

.user .sort-title h2 {
  position: absolute;
  left: 72%;
  top: 17%;
  font-size: 17px;
  font-family: "Lucida Sans", "Lucida Sans Regular", "Lucida Grande",
  "Lucida Sans Unicode", Geneva, Verdana, sans-serif;
  color: #000000;
}

.user .search {
  position: absolute;
  left: 24%;
  top: 15%;
  width: 38%;
}

.user .search_button {
  position: absolute;
  left: 63%;
  top: 16%;
}

.user .sort {
  position: absolute;
  left: 78%;
  top: 15%;
  width: 11%;
}

.user .table_pagination {
  position: absolute;
  left: 45%;
  top: 620px;
}

.el-radio{
  line-height: 25px;
  white-space: normal;
  margin-right: 25px;
  width: 115px;
}

</style>
