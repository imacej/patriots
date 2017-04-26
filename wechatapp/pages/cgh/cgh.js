//index.js
//获取应用实例
var app = getApp()
Page({
  data: {
    motto: 'cgh = cape of good hope 好望角',
    description: '好望角是寻找通往『黄金乐土』的海上通道，终年大风大浪，所谓生活，就是要乘风破浪冲向新大陆嘛。',
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
