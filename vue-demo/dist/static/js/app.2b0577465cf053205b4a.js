webpackJsonp([1],{Dw3o:function(t,e){},NHnr:function(t,e,s){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var n=s("7+uW"),i={render:function(){var t=this.$createElement,e=this._self._c||t;return e("div",{attrs:{id:"app"}},[e("router-view")],1)},staticRenderFns:[]};var a=s("VU/8")({name:"App"},i,!1,function(t){s("bxGm")},null,null).exports,o=s("/ocq"),l={name:"MainPage",data:function(){return{modelList:[{value:"Model1",label:"Model1"},{value:"Model2",label:"Model2"}],isShowSidebar:!1,menuButtonList:[{title:"New chat",icon:"el-icon-edit",click:"newChat"},{title:"Workspace",icon:"el-icon-menu",click:"openWorkspace"}],selectModel:"Model1"}},methods:{handleSidebarShow:function(){this.isShowSidebar=!this.isShowSidebar,this.$refs.sidebar.$el.style.display=this.isShowSidebar?"block":"none"},MenuClick:function(t){var e=t.click;e&&"function"==typeof this[e]&&this[e]()},newChat:function(){console.log("New chat!")},openWorkspace:function(){console.log("Open workspace!")},sendMessage:function(t){console.log("Send message:",t),this.$router.push({path:"/chat",query:t})}}},c={render:function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("el-container",{staticClass:"main-page"},[s("el-aside",{ref:"sidebar",staticClass:"sidebar",attrs:{width:"250px"}},t._l(t.menuButtonList,function(e,n){return s("div",{key:n,staticClass:"menu-item",on:{click:function(s){return t.MenuClick(e)}}},[s("span",{class:e.icon}),t._v("\n      "+t._s(e.title)+"\n    ")])}),0),t._v(" "),s("el-container",[s("el-header",[s("div",{staticClass:"top-bar"},[s("div",{staticClass:"left"},[s("div",{staticClass:"menu-icon el-icon-s-operation button",attrs:{title:"Menu"},on:{click:function(e){return t.handleSidebarShow()}}}),t._v(" "),[s("el-select",{attrs:{filterable:"",placeholder:"Select a model"},model:{value:t.selectModel,callback:function(e){t.selectModel=e},expression:"selectModel"}},t._l(t.modelList,function(t){return s("el-option",{key:t.value,attrs:{label:t.label,value:t.value}})}),1)]],2),t._v(" "),s("div",{staticClass:"right"},[s("div",{staticClass:"el-icon-edit button",attrs:{title:"New chat"},on:{click:function(e){return t.newChat()}}}),t._v(" "),s("div",{staticClass:"el-icon-bell button",attrs:{title:"Settings"}})])])]),t._v(" "),s("el-main",[s("router-view",{attrs:{selectModel:t.selectModel},on:{"send-message":t.sendMessage}})],1)],1)],1)},staticRenderFns:[]};var r=s("VU/8")(l,c,!1,function(t){s("Dw3o")},"data-v-f4be5b94",null).exports,u={mounted:function(){console.log(this.$route.query),this.messageList.push({text:this.$route.query.userInput,isUser:!0}),this.botAnswer()},data:function(){return{userInput:"",messageList:[{text:"Send me messages!",isUser:!1}]}},methods:{moreOptions:function(){console.log("more options")},sendMessage:function(){var t=this;this.messageList.push({text:this.userInput,isUser:!0}),this.userInput="",setTimeout(function(){t.botAnswer()},500)},botAnswer:function(){this.messageList.push({text:"I am a bot!",isUser:!1}),console.log(this.messageList)}}},d={render:function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"chat-page-container"},[s("div",{staticClass:"messages-container"},t._l(t.messageList,function(e,n){return s("div",{key:n,staticClass:"message-item",class:{"user-message":e.isUser,"bot-message":!e.isUser}},[e.isUser?t._e():s("i",{staticClass:"el-icon-s-opportunity"}),t._v("\n            "+t._s(e.text)+"\n            "),e.isUser?s("i",{staticClass:"el-icon-s-custom"}):t._e()])}),0),t._v(" "),s("div",{staticClass:"inputbar"},[s("el-card",{staticClass:"input-section",attrs:{shadow:"never"}},[s("el-input",{attrs:{type:"textarea",autosize:"",placeholder:"Enter your question"},model:{value:t.userInput,callback:function(e){t.userInput=e},expression:"userInput"}}),t._v(" "),s("div",{staticClass:"input-buttons"},[s("div",{staticClass:"more-options el-icon-plus button",attrs:{title:"More"},on:{click:t.moreOptions}}),t._v(" "),s("div",{staticClass:"send-message el-icon-top button",attrs:{title:"Send message"},on:{click:t.sendMessage}})])],1)],1)])},staticRenderFns:[]};var p=s("VU/8")(u,d,!1,function(t){s("PPFZ")},"data-v-68035995",null).exports,m={name:"BlankPage",props:["selectModel"],data:function(){return{userInput:"",suggList:[{title:"Help me study",text:"Vocabulary for a college entrance exam"},{title:"Explain options trading",text:"Explain options trading in simple terms if I'm familiar with buying and selling stocks."},{title:"Tell me a fun fact",text:"Tell me a random fun fact about the Roman Empire"}]}},methods:{sendMessage:function(){this.$emit("send-message",{model:this.selectModel,userInput:this.userInput})},moreOptions:function(){console.log("more options")}},watch:{}},v={render:function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"content-container"},[s("div",{staticClass:"content"},[s("div",{staticClass:"title"},[s("i",{staticClass:"el-icon-s-promotion",staticStyle:{"margin-right":"10px"}}),t._v(t._s(t.selectModel))]),t._v(" "),s("el-card",{staticClass:"input-section",attrs:{shadow:"never"}},[s("el-input",{attrs:{type:"textarea",autosize:"",placeholder:"Enter your question"},model:{value:t.userInput,callback:function(e){t.userInput=e},expression:"userInput"}}),t._v(" "),s("div",{staticClass:"input-buttons"},[s("div",{staticClass:"more-options el-icon-plus button",attrs:{title:"More"},on:{click:t.moreOptions}}),t._v(" "),s("div",{staticClass:"send-message el-icon-top button",attrs:{title:"Send message"},on:{click:t.sendMessage}})])],1),t._v(" "),s("div",{staticClass:"suggestions"},[t._m(0),t._v(" "),t._l(t.suggList,function(e,n){return s("el-card",{key:n,staticClass:"box-card",attrs:{shadow:"hover"},nativeOn:{click:function(s){t.userInput=e.text}}},[s("div",{staticClass:"clearfix",attrs:{slot:"header"},slot:"header"},[s("span",[t._v(t._s(e.title))])]),t._v(" "),s("span",[t._v(t._s(e.text))])])})],2)],1)])},staticRenderFns:[function(){var t=this.$createElement,e=this._self._c||t;return e("p",{staticStyle:{margin:"0","font-size":"14px",color:"#c1c1c1"}},[e("i",{staticClass:"el-icon-magic-stick"}),this._v(" suggested\n            ")])}]};var h=s("VU/8")(m,v,!1,function(t){s("f2I5")},"data-v-19bbb276",null).exports;n.default.use(o.a);var f=new o.a({routes:[{path:"/",name:"MainPage",component:r,children:[{path:"",redirect:"blank"},{path:"blank",name:"BlankPage",component:h},{path:"chat",name:"ChatPage",component:p}]}]}),g=s("zL8q"),b=s.n(g);s("tvR6");n.default.config.productionTip=!1,n.default.use(b.a),new n.default({el:"#app",router:f,components:{App:a},template:"<App/>"})},PPFZ:function(t,e){},bxGm:function(t,e){},f2I5:function(t,e){},tvR6:function(t,e){}},["NHnr"]);
//# sourceMappingURL=app.2b0577465cf053205b4a.js.map