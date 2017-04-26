//index.js
//获取应用实例
var app = getApp()
Page({
  data: {
    motto: 'bmm = book movie music 书影音',
    description: '人嘛，总得有点精神追求。我这个人爱好不算多，基本就是书影音和游戏，在这里分享给大家。',
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
