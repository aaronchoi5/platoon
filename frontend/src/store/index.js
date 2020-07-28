import Vue from "vue";
import Vuex from "vuex";
 
Vue.use(Vuex);
 
export default new Vuex.Store({
 state: {
 	username:'',
 	gameId: '',
 	connection: undefined
 },
 getters: {},
 mutations: {
 	assignUser(state, username){
 		state.username = username;
 	},
 	assignGameId(state, gameId){
 		state.gameId = gameId;
 	},
 	assignConnection(state, connection){
 		state.connection = connection;
 	}
 },
 actions: {}
});