<template>
    <div class="flex items-center space-x-4">
        <img class="profile-image" :src="photo" />
        <h1 class="text-3xl pl-4">{{ member?.name }}</h1>
        <h3 class="text-3xl pl-2">Attendance: {{ presencePercentage }}%</h3>
    </div>
    <Separator class="my-4" />
    <Table>
        <TableHeader>
            <TableRow>
                <TableHead>Date</TableHead>
                <TableHead>Presence</TableHead>
                <TableHead>Image</TableHead>
            </TableRow>
        </TableHeader>
        <TableBody>
            <TableRow v-for="date in presence" :key="date[0]">
                <TableCell class="font-medium">
                    {{ formatDate(date[0]) }}
                </TableCell>
                <TableCell>{{ date[1] ? 'Present' : 'Absent' }}</TableCell>
                <TableCell>
                    <Button class="p-0" variant="link" :disabled="!date[1]" @click="viewImage(date[1])">
                        View
                    </Button>
                </TableCell>
            </TableRow>
        </TableBody>
    </Table>
    <Toaster />
    <div v-if="isModalVisible" class="modal-overlay" @click="handleOverlayClick">
        <div class="modal-content" @click.stop>
            <img :src="modalImage" alt="Modal Image" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useToast } from '@/components/ui/toast/use-toast'
import Toaster from '@/components/ui/toast/Toaster.vue'
import { Button } from '@/components/ui/button'
import { Separator } from '@/components/ui/separator'
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from '@/components/ui/table'

const { toast } = useToast()

const props = defineProps({
    id: String,
});

const member = ref()
const presence = ref()
const presencePercentage = ref()
const photo = ref()
const isModalVisible = ref(false)
const modalImage = ref('')
const showOnlySundays = ref()

onMounted(async () => {
    let response;
    try {
        response = await fetch(`http://localhost:5003/api/settings`)
        const { show_only_sundays } = (await response.json()).data
        showOnlySundays.value = show_only_sundays

        response = await fetch(`http://localhost:5003/api/members/${props.id}`)
        member.value = (await response.json()).data
        photo.value = await fetchImage(member.value.photos.FRONT)
        presence.value = getDates(member.value.calendar, showOnlySundays.value)
        presencePercentage.value = calculatePresence(presence.value, showOnlySundays.value)

    } catch (e: any) {
        console.error(`Failed to fetch member: ${e.message}`);
        toast({
            title: `Failed to fetch member`,
            variant: 'destructive'
        });
    }
})

const getDates = (calendar: Array<Record<string, string>>, showOnlySundays: boolean) => {
    const today = new Date();
    return calendar
        .flatMap(entry => Object.entries(entry))
        .filter(([timestamp]) => {
            const day = new Date(parseInt(timestamp) * 1000);
            const isSunday = day.getDay() === 0;
            const isBeforeToday = day <= today;
            return showOnlySundays
                ? isSunday && isBeforeToday
                : isBeforeToday;
        })
        .reverse();
};

const formatDate = (timestamp: string) => {
    const date = new Date(parseInt(timestamp) * 1000);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
    });
};

const calculatePresence = (calendar: Array<Record<string, string>>, showOnlySundays: boolean) => {
    const today = new Date();
    const startOfYear = new Date(today.getFullYear(), 0, 1);

    let totalDays = 0;
    for (let date = startOfYear; date <= today; date.setDate(date.getDate() + 1)) {
        if (showOnlySundays) {
            if (date.getDay() === 0) {
                totalDays++;
            }
        } else {
            totalDays++;
        }
    }

    const daysPresent = calendar.filter(entry => {
        const [timestamp] = Object.keys(entry);
        const day = new Date(parseInt(timestamp) * 1000);
        if (showOnlySundays) {
            return day.getDay() === 0;
        }
        return true;
    }).length;

    return totalDays === 0 ? 0 : (daysPresent / totalDays) * 100;
};

const fetchImage = async (imageId: string) => {
    const imageResponse = await fetch(`http://localhost:5003/api/images/${imageId}`);
    const imageBlob = await imageResponse.blob();
    return URL.createObjectURL(imageBlob);
}

const viewImage = async (imageId: string) => {
    try {
        modalImage.value = await fetchImage(imageId);
        document.addEventListener('keydown', handleKeyDown);
        isModalVisible.value = true;
    } catch (e: any) {
        console.error(`Failed to fetch image: ${e.message}`);
        toast({
            title: `Failed to fetch image`,
            variant: 'destructive'
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
.profile-image {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    object-fit: cover;
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
    width: 50%;
    height: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
</style>
