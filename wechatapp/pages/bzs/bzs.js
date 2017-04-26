//index.js
//获取应用实例
var app = getApp()
Page({
  data: {
    motto: 'bzs = 不周山',
    description: '学习知识就像不周山，永远不会有『周全』的一天，是为活到老，学到老。',
    userInfo: {}
  },
  //事件处理函数
  bindViewTap: function() {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  onLoad: function () {
    console.log('onLoad')
    var that = this
    //调用应用实例的方法获取全局数据
    app.getUserInfo(function(userInfo){
      //更新数据
      that.setData({
        userInfo:userInfo
      })
    })
  }
})
