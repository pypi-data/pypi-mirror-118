(self.webpackChunkjupyter_bifrost=self.webpackChunkjupyter_bifrost||[]).push([[317,697,581,437],{5318:e=>{e.exports=function(e){return e&&e.__esModule?e:{default:e}},e.exports.default=e.exports,e.exports.__esModule=!0},4088:e=>{e.exports=function(){for(var e=arguments.length,t=[],n=0;n<e;n++)t[n]=arguments[n];if(0!==(t=t.filter((function(e){return null!=e}))).length)return 1===t.length?t[0]:t.reduce((function(e,t){return function(){e.apply(this,arguments),t.apply(this,arguments)}}))}},8141:(e,t,n)=>{"use strict";var r=n(5318);t.__esModule=!0,t.default=function(e,t){e.classList?e.classList.add(t):(0,o.default)(e,t)||("string"==typeof e.className?e.className=e.className+" "+t:e.setAttribute("class",(e.className&&e.className.baseVal||"")+" "+t))};var o=r(n(9077));e.exports=t.default},9077:(e,t)=>{"use strict";t.__esModule=!0,t.default=function(e,t){return e.classList?!!t&&e.classList.contains(t):-1!==(" "+(e.className.baseVal||e.className)+" ").indexOf(" "+t+" ")},e.exports=t.default},602:e=>{"use strict";function t(e,t){return e.replace(new RegExp("(^|\\s)"+t+"(?:\\s|$)","g"),"$1").replace(/\s+/g," ").replace(/^\s*|\s*$/g,"")}e.exports=function(e,n){e.classList?e.classList.remove(n):"string"==typeof e.className?e.className=t(e.className,n):e.setAttribute("class",t(e.className&&e.className.baseVal||"",n))}},702:(e,t,n)=>{"use strict";var r=n(5318);t.__esModule=!0,t.default=t.animationEnd=t.animationDelay=t.animationTiming=t.animationDuration=t.animationName=t.transitionEnd=t.transitionDuration=t.transitionDelay=t.transitionTiming=t.transitionProperty=t.transform=void 0;var o,i,a,s,u,l,p,c,f,d,m,h=r(n(139)),y="transform";if(t.transform=y,t.animationEnd=a,t.transitionEnd=i,t.transitionDelay=p,t.transitionTiming=l,t.transitionDuration=u,t.transitionProperty=s,t.animationDelay=m,t.animationTiming=d,t.animationDuration=f,t.animationName=c,h.default){var v=function(){for(var e,t,n=document.createElement("div").style,r={O:function(e){return"o"+e.toLowerCase()},Moz:function(e){return e.toLowerCase()},Webkit:function(e){return"webkit"+e},ms:function(e){return"MS"+e}},o=Object.keys(r),i="",a=0;a<o.length;a++){var s=o[a];if(s+"TransitionProperty"in n){i="-"+s.toLowerCase(),e=r[s]("TransitionEnd"),t=r[s]("AnimationEnd");break}}return!e&&"transitionProperty"in n&&(e="transitionend"),!t&&"animationName"in n&&(t="animationend"),n=null,{animationEnd:t,transitionEnd:e,prefix:i}}();o=v.prefix,t.transitionEnd=i=v.transitionEnd,t.animationEnd=a=v.animationEnd,t.transform=y=o+"-"+y,t.transitionProperty=s=o+"-transition-property",t.transitionDuration=u=o+"-transition-duration",t.transitionDelay=p=o+"-transition-delay",t.transitionTiming=l=o+"-transition-timing-function",t.animationName=c=o+"-animation-name",t.animationDuration=f=o+"-animation-duration",t.animationTiming=d=o+"-animation-delay",t.animationDelay=m=o+"-animation-timing-function"}var g={transform:y,end:i,property:s,timing:l,delay:p,duration:u};t.default=g},139:(e,t)=>{"use strict";t.__esModule=!0,t.default=void 0;var n=!("undefined"==typeof window||!window.document||!window.document.createElement);t.default=n,e.exports=t.default},5177:(e,t,n)=>{"use strict";var r=n(5318);t.__esModule=!0,t.default=void 0;var o,i=r(n(139)),a="clearTimeout",s=function(e){var t=(new Date).getTime(),n=Math.max(0,16-(t-l)),r=setTimeout(e,n);return l=t,r},u=function(e,t){return e+(e?t[0].toUpperCase()+t.substr(1):t)+"AnimationFrame"};i.default&&["","webkit","moz","o","ms"].some((function(e){var t=u(e,"request");if(t in window)return a=u(e,"cancel"),s=function(e){return window[t](e)}}));var l=(new Date).getTime();(o=function(e){return s(e)}).cancel=function(e){window[a]&&"function"==typeof window[a]&&window[a](e)};var p=o;t.default=p,e.exports=t.default},2703:(e,t,n)=>{"use strict";var r=n(414);function o(){}function i(){}i.resetWarningCache=o,e.exports=function(){function e(e,t,n,o,i,a){if(a!==r){var s=new Error("Calling PropTypes validators directly is not supported by the `prop-types` package. Use PropTypes.checkPropTypes() to call them. Read more at http://fb.me/use-check-prop-types");throw s.name="Invariant Violation",s}}function t(){return e}e.isRequired=e;var n={array:e,bool:e,func:e,number:e,object:e,string:e,symbol:e,any:e,arrayOf:t,element:e,elementType:e,instanceOf:t,node:e,objectOf:t,oneOf:t,oneOfType:t,shape:t,exact:t,checkPropTypes:i,resetWarningCache:o};return n.PropTypes=n,n}},5697:(e,t,n)=>{e.exports=n(2703)()},414:e=>{"use strict";e.exports="SECRET_DO_NOT_PASS_THIS_OR_YOU_WILL_BE_FIRED"},1174:(e,t,n)=>{"use strict";t.__esModule=!0;var r=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},o=l(n(6271)),i=l(n(5697)),a=l(n(2381)),s=l(n(7980)),u=n(4726);function l(e){return e&&e.__esModule?e:{default:e}}function p(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function c(e,t){if(!e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return!t||"object"!=typeof t&&"function"!=typeof t?e:t}u.nameShape.isRequired,i.default.bool,i.default.bool,i.default.bool,(0,u.transitionTimeout)("Appear"),(0,u.transitionTimeout)("Enter"),(0,u.transitionTimeout)("Leave");var f=function(e){function t(){var n,r;p(this,t);for(var i=arguments.length,a=Array(i),u=0;u<i;u++)a[u]=arguments[u];return n=r=c(this,e.call.apply(e,[this].concat(a))),r._wrapChild=function(e){return o.default.createElement(s.default,{name:r.props.transitionName,appear:r.props.transitionAppear,enter:r.props.transitionEnter,leave:r.props.transitionLeave,appearTimeout:r.props.transitionAppearTimeout,enterTimeout:r.props.transitionEnterTimeout,leaveTimeout:r.props.transitionLeaveTimeout},e)},c(r,n)}return function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function, not "+typeof t);e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,enumerable:!1,writable:!0,configurable:!0}}),t&&(Object.setPrototypeOf?Object.setPrototypeOf(e,t):e.__proto__=t)}(t,e),t.prototype.render=function(){return o.default.createElement(a.default,r({},this.props,{childFactory:this._wrapChild}))},t}(o.default.Component);f.displayName="CSSTransitionGroup",f.propTypes={},f.defaultProps={transitionAppear:!1,transitionEnter:!0,transitionLeave:!0},t.default=f,e.exports=t.default},7980:(e,t,n)=>{"use strict";t.__esModule=!0;var r=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},o=f(n(8141)),i=f(n(602)),a=f(n(5177)),s=n(702),u=f(n(6271)),l=f(n(5697)),p=n(4456),c=n(4726);function f(e){return e&&e.__esModule?e:{default:e}}function d(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function m(e,t){if(!e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return!t||"object"!=typeof t&&"function"!=typeof t?e:t}var h=[];s.transitionEnd&&h.push(s.transitionEnd),s.animationEnd&&h.push(s.animationEnd),l.default.node,c.nameShape.isRequired,l.default.bool,l.default.bool,l.default.bool,l.default.number,l.default.number,l.default.number;var y=function(e){function t(){var n,r;d(this,t);for(var o=arguments.length,i=Array(o),a=0;a<o;a++)i[a]=arguments[a];return n=r=m(this,e.call.apply(e,[this].concat(i))),r.componentWillAppear=function(e){r.props.appear?r.transition("appear",e,r.props.appearTimeout):e()},r.componentWillEnter=function(e){r.props.enter?r.transition("enter",e,r.props.enterTimeout):e()},r.componentWillLeave=function(e){r.props.leave?r.transition("leave",e,r.props.leaveTimeout):e()},m(r,n)}return function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function, not "+typeof t);e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,enumerable:!1,writable:!0,configurable:!0}}),t&&(Object.setPrototypeOf?Object.setPrototypeOf(e,t):e.__proto__=t)}(t,e),t.prototype.componentWillMount=function(){this.classNameAndNodeQueue=[],this.transitionTimeouts=[]},t.prototype.componentWillUnmount=function(){this.unmounted=!0,this.timeout&&clearTimeout(this.timeout),this.transitionTimeouts.forEach((function(e){clearTimeout(e)})),this.classNameAndNodeQueue.length=0},t.prototype.transition=function(e,t,n){var r=(0,p.findDOMNode)(this);if(r){var a=this.props.name[e]||this.props.name+"-"+e,u=this.props.name[e+"Active"]||a+"-active",l=null,c=void 0;(0,o.default)(r,a),this.queueClassAndNode(u,r);var f=function(e){e&&e.target!==r||(clearTimeout(l),c&&c(),(0,i.default)(r,a),(0,i.default)(r,u),c&&c(),t&&t())};n?(l=setTimeout(f,n),this.transitionTimeouts.push(l)):s.transitionEnd&&(c=function(e,t){return h.length?h.forEach((function(n){return e.addEventListener(n,t,!1)})):setTimeout(t,0),function(){h.length&&h.forEach((function(n){return e.removeEventListener(n,t,!1)}))}}(r,f))}else t&&t()},t.prototype.queueClassAndNode=function(e,t){var n=this;this.classNameAndNodeQueue.push({className:e,node:t}),this.rafHandle||(this.rafHandle=(0,a.default)((function(){return n.flushClassNameAndNodeQueue()})))},t.prototype.flushClassNameAndNodeQueue=function(){this.unmounted||this.classNameAndNodeQueue.forEach((function(e){e.node.scrollTop,(0,o.default)(e.node,e.className)})),this.classNameAndNodeQueue.length=0,this.rafHandle=null},t.prototype.render=function(){var e=r({},this.props);return delete e.name,delete e.appear,delete e.enter,delete e.leave,delete e.appearTimeout,delete e.enterTimeout,delete e.leaveTimeout,delete e.children,u.default.cloneElement(u.default.Children.only(this.props.children),e)},t}(u.default.Component);y.displayName="CSSTransitionGroupChild",y.propTypes={},t.default=y,e.exports=t.default},2381:(e,t,n)=>{"use strict";t.__esModule=!0;var r=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},o=u(n(4088)),i=u(n(6271)),a=u(n(5697)),s=(u(n(5124)),n(537));function u(e){return e&&e.__esModule?e:{default:e}}a.default.any,a.default.func,a.default.node;var l=function(e){function t(n,o){!function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,t);var i=function(e,t){if(!e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return!t||"object"!=typeof t&&"function"!=typeof t?e:t}(this,e.call(this,n,o));return i.performAppear=function(e,t){i.currentlyTransitioningKeys[e]=!0,t.componentWillAppear?t.componentWillAppear(i._handleDoneAppearing.bind(i,e,t)):i._handleDoneAppearing(e,t)},i._handleDoneAppearing=function(e,t){t.componentDidAppear&&t.componentDidAppear(),delete i.currentlyTransitioningKeys[e];var n=(0,s.getChildMapping)(i.props.children);n&&n.hasOwnProperty(e)||i.performLeave(e,t)},i.performEnter=function(e,t){i.currentlyTransitioningKeys[e]=!0,t.componentWillEnter?t.componentWillEnter(i._handleDoneEntering.bind(i,e,t)):i._handleDoneEntering(e,t)},i._handleDoneEntering=function(e,t){t.componentDidEnter&&t.componentDidEnter(),delete i.currentlyTransitioningKeys[e];var n=(0,s.getChildMapping)(i.props.children);n&&n.hasOwnProperty(e)||i.performLeave(e,t)},i.performLeave=function(e,t){i.currentlyTransitioningKeys[e]=!0,t.componentWillLeave?t.componentWillLeave(i._handleDoneLeaving.bind(i,e,t)):i._handleDoneLeaving(e,t)},i._handleDoneLeaving=function(e,t){t.componentDidLeave&&t.componentDidLeave(),delete i.currentlyTransitioningKeys[e];var n=(0,s.getChildMapping)(i.props.children);n&&n.hasOwnProperty(e)?i.keysToEnter.push(e):i.setState((function(t){var n=r({},t.children);return delete n[e],{children:n}}))},i.childRefs=Object.create(null),i.state={children:(0,s.getChildMapping)(n.children)},i}return function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function, not "+typeof t);e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,enumerable:!1,writable:!0,configurable:!0}}),t&&(Object.setPrototypeOf?Object.setPrototypeOf(e,t):e.__proto__=t)}(t,e),t.prototype.componentWillMount=function(){this.currentlyTransitioningKeys={},this.keysToEnter=[],this.keysToLeave=[]},t.prototype.componentDidMount=function(){var e=this.state.children;for(var t in e)e[t]&&this.performAppear(t,this.childRefs[t])},t.prototype.componentWillReceiveProps=function(e){var t=(0,s.getChildMapping)(e.children),n=this.state.children;for(var r in this.setState({children:(0,s.mergeChildMappings)(n,t)}),t){var o=n&&n.hasOwnProperty(r);!t[r]||o||this.currentlyTransitioningKeys[r]||this.keysToEnter.push(r)}for(var i in n){var a=t&&t.hasOwnProperty(i);!n[i]||a||this.currentlyTransitioningKeys[i]||this.keysToLeave.push(i)}},t.prototype.componentDidUpdate=function(){var e=this,t=this.keysToEnter;this.keysToEnter=[],t.forEach((function(t){return e.performEnter(t,e.childRefs[t])}));var n=this.keysToLeave;this.keysToLeave=[],n.forEach((function(t){return e.performLeave(t,e.childRefs[t])}))},t.prototype.render=function(){var e=this,t=[],n=function(n){var r=e.state.children[n];if(r){var a="string"!=typeof r.ref,s=e.props.childFactory(r),u=function(t){e.childRefs[n]=t};s===r&&a&&(u=(0,o.default)(r.ref,u)),t.push(i.default.cloneElement(s,{key:n,ref:u}))}};for(var a in this.state.children)n(a);var s=r({},this.props);return delete s.transitionLeave,delete s.transitionName,delete s.transitionAppear,delete s.transitionEnter,delete s.childFactory,delete s.transitionLeaveTimeout,delete s.transitionEnterTimeout,delete s.transitionAppearTimeout,delete s.component,i.default.createElement(this.props.component,s,t)},t}(i.default.Component);l.displayName="TransitionGroup",l.propTypes={},l.defaultProps={component:"span",childFactory:function(e){return e}},t.default=l,e.exports=t.default},4317:(e,t,n)=>{"use strict";var r=i(n(1174)),o=i(n(2381));function i(e){return e&&e.__esModule?e:{default:e}}e.exports={TransitionGroup:o.default,CSSTransitionGroup:r.default}},5124:e=>{"use strict";e.exports=function(){}},537:(e,t,n)=>{"use strict";t.__esModule=!0,t.getChildMapping=function(e){if(!e)return e;var t={};return r.Children.map(e,(function(e){return e})).forEach((function(e){t[e.key]=e})),t},t.mergeChildMappings=function(e,t){function n(n){return t.hasOwnProperty(n)?t[n]:e[n]}e=e||{},t=t||{};var r={},o=[];for(var i in e)t.hasOwnProperty(i)?o.length&&(r[i]=o,o=[]):o.push(i);var a=void 0,s={};for(var u in t){if(r.hasOwnProperty(u))for(a=0;a<r[u].length;a++){var l=r[u][a];s[r[u][a]]=n(l)}s[u]=n(u)}for(a=0;a<o.length;a++)s[o[a]]=n(o[a]);return s};var r=n(6271)},4726:(e,t,n)=>{"use strict";t.__esModule=!0,t.nameShape=void 0,t.transitionTimeout=function(e){var t="transition"+e+"Timeout",n="transition"+e;return function(e){if(e[n]){if(null==e[t])return new Error(t+" wasn't supplied to CSSTransitionGroup: this can cause unreliable animations and won't be supported in a future version of React. See https://fb.me/react-animation-transition-group-timeout for more information.");if("number"!=typeof e[t])return new Error(t+" must be a number (in milliseconds)")}return null}},o(n(6271));var r=o(n(5697));function o(e){return e&&e.__esModule?e:{default:e}}t.nameShape=r.default.oneOfType([r.default.string,r.default.shape({enter:r.default.string,leave:r.default.string,active:r.default.string}),r.default.shape({enter:r.default.string,enterActive:r.default.string,leave:r.default.string,leaveActive:r.default.string,appear:r.default.string,appearActive:r.default.string})])}}]);