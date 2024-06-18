<template>
    <div class="cards-container">
        <Dialog v-model:open="isModalOpen">
            <Card key=new class="card">
                <CardContent class="card-content">
                    <DialogTrigger as-child>
                        <PlusCircleIcon class="new-card" draggable="false" style="cursor: pointer"
                            @click="clearActiveCard" />
                    </DialogTrigger>
                </CardContent>
            </Card>
            <Card v-for="card in cards" :key=card.id class="card">
                <CardHeader class="card-header">
                    <CardTitle class="card-title">{{ card.name }}</CardTitle>
                </CardHeader>
                <CardContent class="card-content">
                    <DialogTrigger as-child>
                        <img :src="card.src" draggable="false" style="cursor: pointer"
                            @click="selectActiveCard(card)" />
                    </DialogTrigger>
                </CardContent>
            </Card>
            <DialogContent class="sm:max-w-[450px]">
                <DialogHeader>
                    <DialogTitle v-if="activeCard.id">Edit profile</DialogTitle>
                    <DialogTitle v-else>New profile</DialogTitle>
                    <DialogDescription v-if="activeCard.id">Make changes to the profile here. Click save when you're
                        done.
                    </DialogDescription>
                    <DialogDescription v-else>Create a new profile here. Click save when you're done.
                    </DialogDescription>
                </DialogHeader>
                <Button variant="secondary" @click="goTo(activeCard.id, activeCard.src)">
                    View Presence Report
                </Button>
                <!-- <Button variant="secondary" @click="goTo(activeCard.id, activeCard.src, true)">
                    View Pending Approvals
                </Button> -->
                <MemberFormComponent :member="activeCard" :create="!hasActiveCard" @updateMember="handleUpdateMember"
                    @deleteMember="handleDeleteMember" />
            </DialogContent>
        </Dialog>
    </div>
    <Toaster />
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router';
import Toaster from '@/components/ui/toast/Toaster.vue'
import { useToast } from '@/components/ui/toast/use-toast'
import { Button } from '@/components/ui/button'
import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
} from '@/components/ui/card'
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from '@/components/ui/dialog'
import MemberFormComponent from '@/components/MemberFormComponent.vue'
import { PlusCircleIcon } from 'lucide-vue-next'

const router = useRouter();
const { toast } = useToast()

const isModalOpen = ref<boolean>(false)
const cards = ref<any>([])
const activeCard = ref<any>(null)
const hasActiveCard = ref<boolean>(false)

onMounted(async () => {
    await updateMembersList();
})

const updateMembersList = async () => {
    const members = await fetchMembers();
    const promises = members.map(async (member: any) => {
        const card: any = {
            id: member.id,
            name: member.name,
            birthDate: member.birth_date,
            email: member.email,
            gender: member.gender,
            isMember: member.is_member,
            ministry: member.ministry,
            phoneNumber: member.phone_number,
            sigi: member.sigi,
        }
        try {
            card.src = await fetchMemberImage(member);
        } catch (e: any) {
            console.error(`Failed to fetch image: ${e.message}`);
        }
        return card;
    })
    cards.value = await Promise.all(promises)
}

const handleUpdateMember = async (updatedMember: any) => {
    const member = buildMemberData(updatedMember);
    await pushMemberData(member);
    await updateMembersList();
    isModalOpen.value = false
}

const selectActiveCard = (card: any) => {
    activeCard.value = card
    hasActiveCard.value = true
}

const clearActiveCard = () => {
    hasActiveCard.value = false
    activeCard.value = {
        id: undefined,
        name: undefined,
        birthDate: undefined,
        email: undefined,
        gender: undefined,
        isMember: undefined,
        ministry: undefined,
        phoneNumber: undefined,
        sigi: undefined,
        src: undefined,
    }
}

const buildMemberData = (member: any) => {
    const formData = new FormData();
    formData.append('id', member.id);
    formData.append('name', member.name);
    formData.append('birth_date', member.birthDate);
    formData.append('email', member.email);
    formData.append('gender', member.gender);
    formData.append('phone_number', member.phoneNumber.toString());
    formData.append('is_member', member.isMember ? "true" : "false");
    formData.append('ministry', member.ministry);
    formData.append('sigi', member.sigi.toString());
    formData.append('FRONT', member.frontPhoto);
    formData.append('LEFT', member.leftPhoto);
    formData.append('RIGHT', member.rightPhoto);
    return formData;
}

const fetchMembers = async () => {
    try {
        const response = await fetch('http://localhost:5003/api/members')
        const { members } = (await response.json()).data
        return members
    } catch (e: any) {
        console.error(`Failed to fetch members: ${e.message}`);
        toast({
            title: `Failed to fetch members`,
            variant: 'destructive'
        });
        return []
    }
}

const fetchMemberImage = async (member: any) => {
    if (member.photos?.FRONT) {
        const imageResponse = await fetch(`http://localhost:5003/api/images/${member.photos.FRONT}`);
        const imageBlob = await imageResponse.blob();
        const imageSrc = URL.createObjectURL(imageBlob);
        return imageSrc;
    }
    console.log(`No image found for member: ${member.id}`);
}

const pushMemberData = async (member: any) => {
    try {
        const response = await fetch(`http://localhost:5003/api/members`, {
            method: hasActiveCard.value ? 'PUT' : 'POST',
            body: member,
        });
        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status} - ${response.body}`);
        }
        return await response.json();
    } catch (e: any) {
        console.error(`Failed to connect to API: ${e.message}`);
        toast({
            title: hasActiveCard.value
                ? `Failed to update member`
                : `Failed to create member`,
            variant: 'destructive'
        });
    }
}

const handleDeleteMember = async (id: string) => {
    try {
        const response = await fetch(`http://localhost:5003/api/members/${id}`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status} - ${response.body}`);
        }
        router.go(0); // TODO: make this better
        return await response.json();
    } catch (e: any) {
        console.error(`Failed to connect to API: ${e.message}`);
        toast({
            title: `Failed to delete member`,
            variant: 'destructive'
        });
    }
}

const goTo = (id: string, image: string, pending = false) => {
    const path = pending ? `/management/${id}/pending` : `/management/${id}`;
    router.push(path);
}
</script>

<style scoped>
.cards-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    padding: 20px;
    justify-content: flex-start;
}

.card {
    width: 200px;
    height: 200px;
    border: 0.5px solid #ccc;
    box-shadow: 0 2px 2px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    overflow: hidden;
}

.card-header {
    width: 100%;
    min-height: 36px;
    padding: 10px;
    overflow-x: auto;
    overflow-y: hidden;
    white-space: nowrap;
}

.card-content {
    width: 100%;
    height: 100%;
    position: relative;
    overflow: hidden;
}

.card-content img {
    object-fit: cover;
    object-position: center;
    position: absolute;
    min-width: 100%;
    min-height: 100%;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.new-card {
    object-fit: cover;
    object-position: center;
    position: absolute;
    min-width: 40%;
    min-height: 40%;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}
</style>
