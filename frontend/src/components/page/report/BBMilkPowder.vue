<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-document"></i> 贝贝奶粉报表</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
    
        <el-row>
            <el-col :span="10">
                <h1> 奶粉 <el-tag type="primary"> {{ date }} 日报</el-tag> </h1>
                <br/>
                <el-row>
                    <el-col :span="8"
                            style="text-align:center;">
                        <p><b><u>提问量 {{ qatotal }}</u></b></p>
                        <div v-for="item in qadetails"> {{ item.text }}({{ item.count }}) </div>
                    </el-col>
                    <el-col :span="8"
                            style="text-align:center;">
                        <p><b><u>热门品牌</u></b></p>
                        <div v-for="item in brands"> {{ item.text }}({{ item.count }}) </div>
                    </el-col>
                    <el-col :span="8"
                            style="text-align:center;">
                        <p><b><u>热门关键词</u></b></p>
                        <div v-for="item in keywords"> {{ item.text }}({{ item.count }}) </div>
                    </el-col>
                </el-row>
            </el-col>
            <el-col :span="14">
                <div class="echarts-l">
                    <IEcharts :option="province"></IEcharts>
                </div>
            </el-col>
        </el-row>
        <el-row>
            <el-col :span="8">
                
                <el-row>
                    <el-col :span="12">
                        <p><b><u>售前情感分析</u></b></p>
                        <div class="echarts-s">
                            <IEcharts :option="prs"></IEcharts>
                        </div>
                    </el-col>
                    <el-col :span="12"
                            style="text-align:center;">
                        <p><b><u>热门关键词</u></b></p>
                        <div v-for="item in prswords"> {{ item.text }}({{ item.count }}) </div>
                    </el-col>
                </el-row>
    
            </el-col>
            <el-col :span="8">
                <el-row>
                    <el-col :span="12">
                        <p><b><u>售中情感分析</u></b></p>
                        <div class="echarts-s">
                            <IEcharts :option="sell"></IEcharts>
                        </div>
                    </el-col>
                    <el-col :span="12"
                            style="text-align:center;">
                        <p><b><u>热门关键词</u></b></p>
                        <div v-for="item in sellwords"> {{ item.text }}({{ item.count }}) </div>
                    </el-col>
                </el-row>
            </el-col>
            <el-col :span="8">
                
                <el-row>
                    <el-col :span="12">
                        <p><b><u>售后情感分析</u></b></p>
                        <div class="echarts-s">
                            <IEcharts :option="afs"></IEcharts>
                        </div>
                    </el-col>
                    <el-col :span="12"
                            style="text-align:center;">
                        <p><b><u>热门关键词</u></b></p>
                        <div v-for="item in afswords"> {{ item.text }}({{ item.count }}) </div>
                    </el-col>
                </el-row>
            </el-col>
        </el-row>
    </div>
</template>

<script>
import IEcharts from 'vue-echarts-v3';
export default {
    components: {
        IEcharts
    },
    data() {
        return {
            visible: false,
            date: '2017.04.09',
            qatotal: 262,
            qadetails: [
                { "text": "售前", "count": 185 },
                { "text": "售中", "count": 11 },
                { "text": "售后", "count": 128 },
                { "text": "全球购", "count": 182 },
            ],
            brands: [
                { "text": "爱他美", "count": 15 },
                { "text": "美素佳儿", "count": 4 },
                { "text": "喜宝", "count": 4 },
                { "text": "君乐宝", "count": 3 },
                { "text": "伊利", "count": 2 }
            ],
            keywords: [
                { "text": "真假", "count": 27 },
                { "text": "辨别", "count": 22 },
                { "text": "爱他美", "count": 15 },
                { "text": "正品", "count": 15 },
                { "text": "收到", "count": 12 },
            ],
            prswords: [
                { "text": "真假", "count": 27 },
                { "text": "辨别", "count": 22 },
                { "text": "正品", "count": 15 },
                { "text": "爱他美", "count": 12 },
                { "text": "没有", "count": 10 },
            ],
            sellwords: [
                { "text": "地址", "count": 3 },
                { "text": "发货", "count": 3 },
                { "text": "保质期", "count":2 },
                { "text": "代购", "count": 1 },
                { "text": "商家", "count": 1 },
            ],
            afswords: [
                { "text": "真假", "count": 27 },
                { "text": "辨别", "count": 22 },
                { "text": "收到", "count": 8 },
                { "text": "打开", "count": 8 },
                { "text": "问题", "count": 8 },
            ],
            province: {
                color: ["#20a0ff", "#13CE66", "#F7BA2A", "#FF4949"],
                title: {
                    text: '全国区域排名'
                },
                xAxis: {
                    data: ["山东", "广东", "福建", "河北", "安徽", "陕西", "浙江", "湖南", "北京", "湖北", "河南", "江苏"]
                },
                yAxis: {},
                series: [
                    {
                        name: "问题数",
                        type: "bar",
                        data: [28, 23, 21, 17, 15, 15, 14, 14, 14, 13, 13, 9],
                        label: {
                            normal: {
                                show: true,
                                position: 'top'
                            }
                        },
                    }
                ]
            },
            prs: {
                color: ["#20a0ff", "#FF4949", "#61a0a8"],
                tooltip: {
                    trigger: 'item',
                    formatter: "{a} <br/>{b} : {c} ({d}%)"
                },
                series: [
                    {
                        name: '售前用户问句情感',
                        type: 'pie',
                        radius: '55%',
                        center: ['50%', '50%'],
                        data: [
                            { value: 163, name: '中性' },
                            { value: 22, name: '消极' },
                        ],
                        itemStyle: {
                            emphasis: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        },
                    }
                ]
            },
            sell: {
                color: ["#20a0ff", "#FF4949", "#61a0a8"],
                tooltip: {
                    trigger: 'item',
                    formatter: "{a} <br/>{b} : {c} ({d}%)"
                },
                series: [
                    {
                        name: '售中用户问句情感',
                        type: 'pie',
                        radius: '55%',
                        center: ['50%', '50%'],
                        data: [
                            { value: 10, name: '中性' },
                            { value: 1, name: '消极' },
                        ],
                        itemStyle: {
                            emphasis: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        }
                    }
                ]
            },
            afs: {
                color: ["#20a0ff", "#FF4949", "#61a0a8"],
                tooltip: {
                    trigger: 'item',
                    formatter: "{a} <br/>{b} : {c} ({d}%)"
                },
                series: [
                    {
                        name: '售后用户问句情感',
                        type: 'pie',
                        radius: '55%',
                        center: ['50%', '50%'],
                        data: [
                            { value: 119, name: '中性' },
                            { value: 9, name: '消极' },
                        ],
                        itemStyle: {
                            emphasis: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        }
                    }
                ]
            },
        }
    },
    methods: {

    }
}
</script>


<style scoped>
.echarts-l {
    width: 100%;
    height: 238px;
}

.echarts-s {
    width: 100%;
    height: 150px;
}


.el-row {
    margin-bottom: 20px;
    &:last-child {
        margin-bottom: 0;
    }
}

.el-col {
    border-radius: 4px;
}

.bg-purple-dark {
    background: #99a9bf;
}

.bg-purple {
    background: #d3dce6;
}

.bg-purple-light {
    background: #e5e9f2;
}

.grid-content {
    border-radius: 4px;
    min-height: 36px;
}

.row-bg {
    padding: 10px 0;
    background-color: #f9fafc;
}
</style>