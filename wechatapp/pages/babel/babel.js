//index.js
//获取应用实例
var app = getApp()
Page({
  data: {
    motto: 'babel = 通天塔',
    description: '工程实践就像通天塔，需要不断添砖加瓦才能越盖越高。',
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
