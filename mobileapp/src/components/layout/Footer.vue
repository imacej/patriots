<template>
    <tabbar>
        <tabbar-item :selected="tabIndex === 0"
                     @on-item-click="handler">
            <img slot="icon"
                 src="../../assets/images/ic_nav_news_normal.png">
            <img slot="icon-active"
                 src="../../assets/images/ic_nav_news_actived.png">
            <span slot="label">综合</span>
        </tabbar-item>
        <tabbar-item :selected="tabIndex === 1"
                     @on-item-click="handler">
            <img slot="icon"
                 src="../../assets/images/ic_nav_tweet_normal.png">
            <img slot="icon-active"
                 src="../../assets/images/ic_nav_tweet_actived.png">
            <span slot="label">动弹</span>
        </tabbar-item>
        <tabbar-item :selected="tabIndex === 2"
                     @on-item-click="handler">
            <img style="height:40px;width:40px;"
                 slot="icon"
                 src="../../assets/images/ic_nav_add_normal.png">
        </tabbar-item>
        <tabbar-item :selected="tabIndex === 3"
                     @on-item-click="handler">
            <img slot="icon"
                 src="../../assets/images/ic_nav_discover_normal.png">
            <img slot="icon-active"
                 src="../../assets/images/ic_nav_discover_actived.png">
            <span slot="label">发现</span>
        </tabbar-item>
        <tabbar-item :selected="tabIndex === 4"
                     @on-item-click="handler">
            <img slot="icon"
                 src="../../assets/images/ic_nav_my_normal.png">
            <img slot="icon-active"
                 src="../../assets/images/ic_nav_my_actived.png">
            <span slot="label">我的</span>
        </tabbar-item>
    </tabbar>
</template>
<style>
.add {
    height: 40px;
    width: 40px;
}
</style>
<script>
import { Tabbar, TabbarItem } from 'vux'
import { mapState } from 'vuex'

export default {
    name: 'AppFooter',
    components: {
        Tabbar,
        TabbarItem,
    },
    computed: mapState({
        // 箭头函数可使代码更简练
        tabIndex: state => state.tabIndex,
    }),
    mounted() {
        console.log(this.tabIndex)
    },
    data() {
        return {
            msg: ''
        }
    },
    methods: {
        handler(index) {
            console.log(index)
            this.$store.commit('changeTab', index)
        }
    }
}

</script>