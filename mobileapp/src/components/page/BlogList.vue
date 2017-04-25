<template>
    <div>
        <counter></counter>
    </div>
</template>
<style>

</style>
<script>
import { mapState } from 'vuex'

const Counter = {
    template: `<div>{{ count }}</div>`,
    computed: mapState({
        // 箭头函数可使代码更简练
        count: state => state.count,

        // 传字符串参数 'count' 等同于 `state => state.count`
        countAlias: 'count',

        // 为了能够使用 `this` 获取局部状态，必须使用常规函数
        countPlusLocalState(state) {
            return state.count + this.localCount
        }
    })
}


export default {
    components: {
        Counter
    },
    name: 'BlogList'
}

</script>
