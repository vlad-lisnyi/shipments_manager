<template>
  <div class="home">
    <h1 class="title">Shipments Manager</h1>

    <hr/>

    <h2 class="subtitle">Add shipment</h2>

    <div class="columns">
      <div class="column">
        <label class="label">Departure:</label>
        <div class="control">
          <input class="input" type="text" v-model="departure">
        </div>
      </div>

      <div class="column">
        <label class="label">Destination:</label>
        <div class="control">
          <input class="input" type="text" v-model="destination">
        </div>
      </div>

      <div class="column">
        <label class="label">Status</label>
        <div class="control">
          <div class="select">
            <select v-model="status">
              <option v-for="st in statuses" :selected="status === st">{{ st }}</option>
            </select>
          </div>
        </div>
      </div>

      <div class="column is-justify-content-end">
        <label class="label is-invisible">Create</label>
        <div class="control">
          <button class="button is-link" @click="addShipment">Create</button>
        </div>
      </div>

    </div>

    <hr/>

    <h2 class="subtitle">Shipments</h2>
    <div class="box" v-if="!shipments.length">No shipments in the inventory</div>
    <div class="box" v-for="shipment in shipments" v-bind:key="shipment.id">
      <div class="columns">
        <div class="column is-narrow">
          <div class="field">
            <label class="label is-invisible">#</label>
            <label>Shipment #{{shipment.id}}</label>
          </div>
        </div>

        <div class="column">
          <div class="field mb-0">
            <label>From </label>
          </div>
          <div class="field">
            <input v-show="!shipment.editable" class="input" type="text" v-bind:value="shipment.departureLocation" disabled=0>
            <input v-show="shipment.editable" class="input" type="text" v-model="shipment.departureLocation" :placeholder="shipment.departureLocation">
          </div>
        </div>

        <div class="column">
          <div class="field mb-0">
            <label> To </label>
            <input v-show="!shipment.editable" class="input" type="text" v-bind:value="shipment.destinationLocation" disabled=0>
            <input v-show="shipment.editable" class="input" type="text" v-model="shipment.destinationLocation" :placeholder="shipment.destinationLocation">
          </div>
        </div>
        
        <div class="column">
          <div class="field">
            <label>Status</label>
            <div class="select" v-show="!shipment.editable" >
              <select v-model="shipment.status" disabled=0>
                <option v-for="st in statuses" :selected="shipment.status === st">{{ st }}</option>
              </select>
            </div>
            <div class="select" v-show="shipment.editable">
              <select v-model="shipment.status">
                <option v-for="st in statuses" :selected="shipment.status === st">{{ st }}</option>
              </select>
            </div>
          </div>
        </div>

        <div class="column is-narrow">
          <label class="label is-invisible mb-0">btns</label>
          <div class="buttons" v-show="!shipment.editable">
            <button class="button is-primary is-light" @click="editShipment(shipment)">Edit</button>
            <button class="button is-danger" @click="deleteShipment(shipment.id)">Delete</button>
          </div>
          <div class="buttons" v-show="shipment.editable">
            <button class="button is-success" @click="updateShipment(shipment)">Accept</button>
            <button class="button is-danger" @click="cancelEdit(shipment)">Cancel</button>
          </div>
        </div>
            
      </div>
    </div>

  </div>
</template>

<script>

import axios from '../../node_modules/axios'

export default {
  name: 'ShipmentsView',
  data () {
    return {
      shipments: [],
      statuses: ["In progress","Completed","Delayed"],
      departure:'',
      destination:'',
      status:"In progress"
    }
  },
  mounted () {
    this.getShipments(),
    this.generateShipmentEditOption()
  },
  methods: {
    getShipments() {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/shipments/',
        auth: {
          username: 'admin',
          password: 'admin'
        }
      }).then(response => this.shipments = response.data)
    },
    generateShipmentEditOption(){
      for(var i=0; i < this.shipments.length; i++){
        shipment = this.shipments[i];
        shipment.editable = false;
        this.shipments.push(shipment)
      }
    },
    addShipment() {
      if (this.destination && this.departure) {
        axios({
          method: 'post',
          url: 'http://127.0.0.1:8000/shipments/',
          data: {
            departureLocation: this.departure,
            destinationLocation: this.destination,
            stats: this.status
          },
          auth: {
            username: 'admin',
            password: 'admin'
          }
        }).then((response) => {
          let newShipment = {
            'id': response.data.id,
            'departureLocation': this.departure,
            'destinationLocation': this.destination,
            'status': this.status
          }

          this.shipments.push(newShipment)

          this.departure = ''
          this.destination = ''
          this.status = 'In progress'
        }).catch((error) => {
          console.log(error)
        })
      }
    },
    editShipment (shipment) {
      this._originalShipment = Object.assign({},shipment);
      shipment.editable = true;
    },
    cancelEdit(shipment) {
      Object.assign(shipment, this._originalShipment);
      shipment.editable = false;
    },
    deleteShipment(shipment_id) {
      axios({
        method: 'delete',
        url: 'http://127.0.0.1:8000/shipments/' + shipment_id + '/',
        headers:{
          'Content-Type': 'application/json',
        },
        auth: {
            username: 'admin',
            password: 'admin'
          }
      }).then(success => {
        location.reload()
      }).catch((error) => {
        console.log(error)
      });
    },
    updateShipment(shipment) {
      console.log(JSON.stringify(shipment,null,2))
      axios({
        method: 'put',
        url: 'http://127.0.0.1:8000/shipments/' + shipment.id + '/',
        headers:{
          'Content-Type': 'application/json',
        },
        data: {
          departureLocation: shipment.departureLocation,
          destinationLocation: shipment.destinationLocation,
          status: shipment.status
        },
        auth: {
            username: 'admin',
            password: 'admin'
          }
      }).then(success => {
        shipment.editable = false;
      }).catch((error) => {
        console.log(error)
      });
    }
  }
}
</script>

<style lang="scss">
.select, select {
  width:100%;
}
</style>