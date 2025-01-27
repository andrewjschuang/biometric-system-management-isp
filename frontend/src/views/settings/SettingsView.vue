<template>
    <form @submit.prevent="handleSubmit">
        <FormField name="videoSource">
            <FormItem class="form-item">
                <FormLabel>Video Source</FormLabel>
                <FormControl class="form-control">
                    <Input type="text" v-model="videoSource" />
                </FormControl>
                <FormMessage />
            </FormItem>
        </FormField>
        <FormField name="tolerance">
            <FormItem class="form-item">
                <FormLabel>Tolerance</FormLabel>
                <FormControl class="form-control">
                    <Input type="number" min="0.1" max="1.0" step="0.01" v-model="tolerance" />
                </FormControl>
                <FormMessage />
            </FormItem>
        </FormField>
        <div class="items-top flex gap-x-2 pl-5 pt-4">
            <TooltipProvider>
                <Tooltip>
                    <TooltipTrigger as-child>
                        <Checkbox id="enableMatchConfirmation" v-model:checked="enableMatchConfirmation"
                            :disabled="true" />
                    </TooltipTrigger>
                    <TooltipContent>
                        <p>Feature currently not supported</p>
                    </TooltipContent>
                </Tooltip>
            </TooltipProvider>
            <div class="grid gap-1.5 leading-none">
                <label for="enableMatchConfirmation"
                    class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                    Enable match confirmation window
                </label>
                <p class="text-sm text-muted-foreground">
                    Show or hide match confirmation photos in home view.
                </p>
            </div>
        </div>
        <div class="items-top flex gap-x-2 pl-5 pt-4">
            <Checkbox id="showOnlySundays" v-model:checked="showOnlySundays" />
            <div class="grid gap-1.5 leading-none">
                <label for="showOnlySundays"
                    class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                    Calendar shows only sundays
                </label>
                <p class="text-sm text-muted-foreground">
                    Toggle between showing all days or only sundays.
                </p>
            </div>
        </div>
        <div class="items-top flex pt-4">
            <div class="button-container">
                <Button type="submit">
                    Save Changes
                </Button>
            </div>
        </div>
    </form>
    <Toaster />
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import {
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage
} from '@/components/ui/form'
import {
    Tooltip,
    TooltipContent,
    TooltipProvider,
    TooltipTrigger,
} from '@/components/ui/tooltip'
import { Checkbox } from '@/components/ui/checkbox'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { useToast } from '@/components/ui/toast/use-toast'
import Toaster from '@/components/ui/toast/Toaster.vue'

const { toast } = useToast()

const videoSource = ref<string>('')
const tolerance = ref<number>()
const enableMatchConfirmation = ref<boolean>()
const showOnlySundays = ref<boolean>()

onMounted(async () => {
    try {
        const configuration = await getRequest('configuration')
        videoSource.value = configuration.video_source
        tolerance.value = configuration.tolerance

        const settings = await getRequest('settings')
        enableMatchConfirmation.value = settings.enable_match_confirmation
        showOnlySundays.value = settings.show_only_sundays
    } catch (e: any) {
        console.error(`Failed to retrieve configuration: ${e.message}`);
        toast({
            title: `Failed to retrieve configuration`,
            variant: 'destructive'
        });
    }
})

const handleSubmit = async () => {
    try {
        await postRequest('configuration', {
            video_source: videoSource.value,
            tolerance: tolerance.value,
        })
        await postRequest('settings', {
            enable_match_confirmation: enableMatchConfirmation.value,
            show_only_sundays: showOnlySundays.value,
        })
        window.location.reload(); // TODO: should not need to reload
        // toast({
        //     title: `Successfully updated configuration`,
        // });
    } catch (e: any) {
        console.error(`Failed to update configuration`);
        toast({
            title: `Failed to update configuration`,
            variant: 'destructive'
        });
    }
}

const getRequest = async (path: string) => {
    const response = await fetch(`http://localhost:5003/api/${path}`)
    return (await response.json()).data
}

const postRequest = async (path: string, data: object) => {
    const response = await fetch(`http://localhost:5003/api/${path}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    })

    if (!response.ok) {
        throw new Error(`HTTP error: ${response.status} - ${response.body}`);
    }
}
</script>

<style scoped>
.form-item {
    padding-left: 20px;
    padding-bottom: 10px;
}

.button-container {
    padding-left: 20px;
}
</style>
