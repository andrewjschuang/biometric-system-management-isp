<template>
    <form @submit.prevent="handleSubmit">
        <FormField v-slot="{ componentField }" name="name">
            <FormItem class="form-item">
                <FormLabel>Name<span v-if="props.create">*</span></FormLabel>
                <FormControl class="form-control">
                    <Input type="text" placeholder="Full Name" v-bind="componentField" v-model="localMember.name"
                        :required="props.create" />
                </FormControl>
                <FormMessage />
            </FormItem>
        </FormField>
        <FormField v-slot="{ componentField }" name="nickname">
            <FormItem class="form-item">
                <FormLabel>Nickname</FormLabel>
                <FormControl class="form-control">
                    <Input type="text" placeholder="Nickname" v-bind="componentField" v-model="localMember.nickname"
                        :required="props.create" />
                </FormControl>
                <FormMessage />
            </FormItem>
        </FormField>
        <FormField v-slot="{ componentField }" name="birthDate">
            <FormItem class="form-item">
                <FormLabel>Birth Date<span v-if="props.create">*</span></FormLabel>
                <FormControl class="form-control">
                    <Input type="text" placeholder="31/12/2000" v-bind="componentField" v-model="localMember.birthDate"
                        :required="props.create" />
                </FormControl>
                <!-- <Popover>
                    <PopoverTrigger as-child>
                        <FormControl class="form-control">
                            <Button variant="outline"
                                :class="cn('w-[240px] ps-3 text-start font-normal', !localMember.birthDate && 'text-muted-foreground')">
                                <span>{{ localMember.birthDate ? format(localMember.birthDate, "PPP") : "Pick a date"
                                    }}</span>
                                <CalendarIcon class="ms-auto h-4 w-4 opacity-50" />
                            </Button>
                        </FormControl>
                    </PopoverTrigger>
                    <PopoverContent class="p-0">
                        <Calendar v-bind="componentField" v-model="localMember.birthDate" />
                    </PopoverContent>
                </Popover> -->
                <FormMessage />
            </FormItem>
        </FormField>
        <FormField v-slot="{ componentField }" name="email">
            <FormItem class="form-item">
                <FormLabel>Email<span v-if="props.create">*</span></FormLabel>
                <FormControl class="form-control">
                    <Input type="text" placeholder="example@email.com" v-bind="componentField"
                        v-model="localMember.email" :required="props.create" />
                </FormControl>
                <FormMessage />
            </FormItem>
        </FormField>
        <FormField v-slot="{ componentField }" name="gender">
            <FormItem class="form-item">
                <FormLabel>Gender<span v-if="props.create">*</span></FormLabel>
                <FormControl class="form-control">
                    <Select :required="props.create" v-bind="componentField" v-model="localMember.gender">
                        <SelectTrigger>
                            <SelectValue :placeholder="localMember.gender || '--'" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectItem value="male">Male</SelectItem>
                                <SelectItem value="female">Female</SelectItem>
                            </SelectGroup>
                        </SelectContent>
                    </Select>
                </FormControl>
                <FormMessage />
            </FormItem>
        </FormField>
        <FormField v-slot="{ componentField }" name="phoneNumber">
            <FormItem class="form-item">
                <FormLabel>Phone Number<span v-if="props.create">*</span></FormLabel>
                <FormControl class="form-control">
                    <Input type="text" placeholder="11912345678" v-bind="componentField"
                        v-model="localMember.phoneNumber" :required="props.create" />
                </FormControl>
                <FormMessage />
            </FormItem>
        </FormField>
        <FormField v-slot="{ value }" name="isMember">
            <FormItem class="form-item">
                <FormLabel>Is Member</FormLabel>
                <FormControl class="form-control">
                    <Switch :checked="value || localMember.isMember"
                        @update:checked="localMember.isMember = $event ?? false" />
                </FormControl>
                <FormMessage />
            </FormItem>
        </FormField>
        <FormField v-slot="{ componentField }" name="ministry">
            <FormItem class="form-item">
                <FormLabel>Ministry<span v-if="props.create">*</span></FormLabel>
                <FormControl class="form-control">
                    <Select :required="props.create" v-bind="componentField" v-model="localMember.ministry">
                        <SelectTrigger>
                            <SelectValue :placeholder="localMember.ministry || '--'" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectItem value="pt">PT</SelectItem>
                                <SelectItem value="tw">TW</SelectItem>
                                <SelectItem value="md">MD</SelectItem>
                            </SelectGroup>
                        </SelectContent>
                    </Select>
                </FormControl>
                <FormMessage />
            </FormItem>
        </FormField>
        <FormField v-slot="{ componentField }" name="sigi">
            <FormItem class="form-item">
                <FormLabel>SIGI</FormLabel>
                <FormControl class="form-control">
                    <Input type="number" placeholder="1" v-bind="componentField" v-model="localMember.sigi" />
                </FormControl>
                <FormMessage />
            </FormItem>
        </FormField>
        <FormField v-if="!props.create" v-slot="{ componentField }" name="isActive">
            <FormItem class="form-item">
                <FormLabel>Is currently active</FormLabel>
                <FormControl class="form-control">
                    <Switch v-bind="componentField" v-model="localMember.isActive" disabled />
                </FormControl>
                <FormMessage />
            </FormItem>
        </FormField>
        <FormField v-slot="{ componentField }" name="frontPhoto">
            <FormItem class="form-item">
                <FormLabel>Front Photo<span v-if="props.create">*</span></FormLabel>
                <FormControl class="form-control">
                    <Input type="file" placeholder="Front Photo" @change="handlePhotoChange($event, 'frontPhoto')"
                        :required="props.create" />
                </FormControl>
                <FormMessage />
            </FormItem>
        </FormField>
        <FormField v-slot="{ componentField }" name="leftPhoto">
            <FormItem class="form-item">
                <FormLabel>Left Photo</FormLabel>
                <FormControl class="form-control">
                    <Input type="file" placeholder="Left Photo" @change="handlePhotoChange($event, 'leftPhoto')" />
                </FormControl>
                <FormMessage />
            </FormItem>
        </FormField>
        <FormField v-slot="{ componentField }" name="rightPhoto">
            <FormItem class="form-item">
                <FormLabel>Right Photo</FormLabel>
                <FormControl class="form-control">
                    <Input type="file" placeholder="Right Photo" @change="handlePhotoChange($event, 'rightPhoto')" />
                </FormControl>
                <FormMessage />
            </FormItem>
        </FormField>
        <div class="button-container">
            <Button type="submit">
                Save Changes
            </Button>
            <AlertDialog v-if="!props.create">
                <AlertDialogTrigger as-child>
                    <Button variant="destructive">
                        Delete Profile
                    </Button>
                </AlertDialogTrigger>
                <AlertDialogContent>
                    <AlertDialogHeader>
                        <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
                        <AlertDialogDescription>
                            This action cannot be undone. This will permanently the profile.
                        </AlertDialogDescription>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                        <AlertDialogCancel>Cancel</AlertDialogCancel>
                        <AlertDialogAction @click="handleDelete">Delete</AlertDialogAction>
                    </AlertDialogFooter>
                </AlertDialogContent>
            </AlertDialog>
        </div>
    </form>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { format } from 'date-fns'
import { Calendar as CalendarIcon } from 'lucide-vue-next'
import { cn } from '@/lib/utils'
import { Calendar } from '@/components/ui/calendar'
import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
    AlertDialogTrigger,
} from '@/components/ui/alert-dialog'
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select'
import { Switch } from '@/components/ui/switch'
import {
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage
} from '@/components/ui/form'
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from '@/components/ui/popover'

import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'


interface Member {
    id: string | undefined;
    name: string;
    nickname: string;
    birthDate: string;
    email: string;
    gender: string;
    phoneNumber: number;
    isMember: boolean;
    ministry: string;
    sigi: number;
    isActive: boolean | undefined;
    frontPhoto: any;
    leftPhoto: any;
    rightPhoto: any;
}

const props = defineProps<{
    member: Member;
    create?: boolean;
}>();

const localMember = ref<Member>({ ...props.member });

const emit = defineEmits(['updateMember', 'deleteMember']);

const handlePhotoChange = (event: any, field: 'frontPhoto' | 'leftPhoto' | 'rightPhoto') => {
    const file = event.target.files[0];
    if (file) localMember.value[field] = file;
    console.log(localMember.value)
}

const handleSubmit = () => {
    emit('updateMember', localMember.value);
}

const handleDelete = () => {
    emit('deleteMember', localMember.value.id)
}
</script>

<style scoped>
.form-item {
    display: flex;
    flex-direction: column;
    margin-bottom: 8px;
}

.form-label,
.form-control {
    display: block;
}

.button-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
</style>
