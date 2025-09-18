<template>
    <div>
        <ul v-if="events.length > 0">
            <li>
                <div class="flex h-5 items-center space-x-4 text-lg">
                    <Label class="flex-1">Date</Label>
                    <Separator orientation="vertical" />
                    <Label class="flex-1">Match</Label>
                    <Separator orientation="vertical" />
                    <Label class="flex-1">Face Distance</Label>
                    <Separator orientation="vertical" />
                    <Label class="flex-1">Event</Label>
                    <Separator orientation="vertical" />
                    <Label class="flex-1">Confirmed</Label>
                    <Separator orientation="vertical" />
                    <Label class="flex-1 text-center">Image</Label>
                </div>
            </li>
            <li v-for="(event, index) in events" :key="index">
                <div class="flex h-5 items-center space-x-4 text-sm">
                    <div class="flex-1 text-gray-600">{{ formatTimestamp(event.timestamp) }}</div>
                    <Separator orientation="vertical" />
                    <div class="flex-1 text-gray-600">{{ event.name }}</div>
                    <Separator orientation="vertical" />
                    <div class="flex-1 text-gray-600">{{ event.face_distance }}</div>
                    <Separator orientation="vertical" />
                    <div class="flex-1 text-gray-600">{{ event.event_name || '' }}</div>
                    <Separator orientation="vertical" />
                    <div class="flex-1 text-gray-600">{{ event.confirmed }}</div>
                    <Separator orientation="vertical" />
                    <Button class="p-0 flex-1 text-center text-sm text-gray-600" variant="link" :disabled="!event.photo" @click="viewImage(event.photo)">
                        View
                    </Button>
                </div>
            </li>
        </ul>
        <p v-else>No events available.</p>
    </div>
    <Toaster />
    <div v-if="isModalVisible" class="modal-overlay" @click="handleOverlayClick">
        <div class="modal-content" @click.stop>
            <img :src="modalImage" alt="Modal Image" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useToast } from '@/components/ui/toast/use-toast';
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import Toaster from '@/components/ui/toast/Toaster.vue';
import { Button } from "@/components/ui/button";

const { toast } = useToast();

const events = ref<any[]>([]);
const isModalVisible = ref(false);
const modalImage = ref('');

onMounted(() => {
    fetchEvents();
});

const fetchEvents = async () => {
    try {
        const startOf2024 = Math.floor(new Date('2024-01-01T00:00:00Z').getTime() / 1000);
        const response = await fetch(`http://localhost:5003/api/events?start_range=${startOf2024}`);
        events.value = (await response.json()).data;
    } catch (error) {
        console.error('Error fetching events:', error);
        toast({
            title: 'Error fetching events',
            variant: 'destructive',
        });
    }
};

const formatTimestamp = (timestamp: number) => {
    const date = new Date(timestamp * 1000);
    const dayName = date.toLocaleDateString('en-US', { weekday: 'long' });
    const datePart = date.toLocaleDateString('en-GB'); // DD/MM/YYYY
    const timePart = date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false });
    return `${datePart} ${timePart} ${dayName}`;
};

const fetchImage = async (imageId: string) => {
    const imageResponse = await fetch(`http://localhost:5003/api/images/${imageId}`);
    const imageBlob = await imageResponse.blob();
    return URL.createObjectURL(imageBlob);
};

const viewImage = async (imageId: string) => {
    try {
        modalImage.value = await fetchImage(imageId);
        isModalVisible.value = true;
        document.addEventListener('keydown', handleKeyDown);
    } catch (e: any) {
        console.error(`Failed to fetch image: ${e.message}`);
        toast({
            title: 'Failed to fetch image',
            variant: 'destructive',
        });
    }
};

const closeModal = () => {
    isModalVisible.value = false;
    document.removeEventListener('keydown', handleKeyDown);
};

const handleOverlayClick = () => {
    closeModal();
};

const handleKeyDown = (event: KeyboardEvent) => {
    if (event.key === 'Escape') {
        closeModal();
    }
};

onBeforeUnmount(() => {
    document.removeEventListener('keydown', handleKeyDown);
});
</script>

<style scoped>
ul {
    list-style: none;
    padding: 0;
}

li {
    padding: 0.5rem 0;
    border-bottom: 1px solid #ddd;
}

.flex-1 {
    flex: 1;
}

.text-center {
    text-align: center;
}

.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
}

.modal-content {
    max-width: 80%;
    max-height: 80%;
}

.modal-content img {
    width: 100%;
    height: auto;
    border-radius: 8px;
}
</style>
