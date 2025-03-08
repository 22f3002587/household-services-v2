<template>
    <div>
        <div class="form">
          <h2 style="margin-bottom: 35px">Add Service</h2>
          <table>
            <tbody>
              <tr>
                <td>
                  <label for="service_cat">Service Category:</label>
                </td>
    
                <td>
                  <select v-model="form.service_category" id="service_cat" required>
                    <option disabled>Select Category</option>
                    <option>Electrician</option>
                    <option>Saloon</option>
                    <option>Health and Wellness</option>
                    <option>Cleaning</option>
                    <option>Home Decoration</option>
                  </select>
                </td>
              </tr>
    
              <tr>
                <td>
                  <label for="service_name">Service Name:</label>
                </td>
                <td>
                  <input type="text" v-model="form.service_name" required />
                </td>
              </tr>
    
              <tr>
                <td>
                  <label for="time">Expected Time</label>
                </td>
                <td>
                  <input type="text" v-model="form.expected_time" required />
                </td>
              </tr>
    
              <tr>
                <td>
                  <label for="description">Add Description:</label>
                </td>
                <td>
                  <textarea v-model="form.description" required></textarea>
                  <!-- <input type="text" v-model="form.description" required /> -->
                </td>
              </tr>
    
              <tr>
                <td>
                  <label for="base_price">Price:</label>
                </td>
                <td>
                  <input type="text" v-model="form.base_price" required />
                </td>
              </tr>
            </tbody>
          </table>
          <button @click="submitData">Submit</button>
          <p v-if="message">{{ message }}</p>
        </div>
      </div>
</template>

<script>


</script>

<style>


</style>