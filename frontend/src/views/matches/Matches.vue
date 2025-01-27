<template>
    <div>
        <h1>Events</h1>
        <ul v-if="events.length > 0">
            <li v-for="(event, index) in events" :key="index">
                {{ formatTimestamp(event.timestamp) }} | {{ event.name }}
            </li>
        </ul>
        <p v-else>No events available.</p>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';

const events = ref<any>([]);

const fetchEvents = async () => {
    try {
        const startOf2024 = Math.floor(new Date('2024-01-01T00:00:00Z').getTime() / 1000);
        const response = await fetch(`http://localhost:5003/api/events?start_range=${startOf2024}`)
        events.value = (await response.json()).data
        console.log(events)
    } catch (error) {
        console.error('Error fetching events:', error);
    }
};

const formatTimestamp = (timestamp: number) => {
    const date = new Date(timestamp * 1000);
    const dayName = date.toLocaleDateString('en-US', { weekday: 'long' });
    const datePart = date.toLocaleDateString('en-GB').replace(/\//g, '/'); // Formats as DD/MM/YYYY
    const timePart = date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false });
    return `${dayName}, ${datePart} ${timePart}`;
};

onMounted(() => {
    fetchEvents();
});
</script>

<style scoped>
h1 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
}

ul {
    list-style: none;
    padding: 0;
}

li {
    padding: 0.5rem 0;
    border-bottom: 1px solid #ddd;
}

p {
    color: gray;
}
</style>
