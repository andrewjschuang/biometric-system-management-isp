<template>
    <div class="items-top flex gap-x-2 pl-5 pt-4">
        <TooltipProvider>
            <Tooltip>
                <TooltipTrigger as-child>
                    <Checkbox id="enableMatchConfirmation" v-model:checked="enableMatchConfirmation" :disabled="true" />
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
    <Toaster />
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import { useToast } from '@/components/ui/toast/use-toast'
import Toaster from '@/components/ui/toast/Toaster.vue'
import { Checkbox } from '@/components/ui/checkbox'
import {
    Tooltip,
    TooltipContent,
    TooltipProvider,
    TooltipTrigger,
} from '@/components/ui/tooltip'

const { toast } = useToast()

const enableMatchConfirmation = ref(false)
const showOnlySundays = ref(false)
const initialized = ref(false)

onMounted(async () => {
    try {
        const response = await fetch(`http://localhost:5003/api/settings`)
        const settings = (await response.json()).data
        enableMatchConfirmation.value = settings.enable_match_confirmation
        showOnlySundays.value = settings.show_only_sundays
        initialized.value = true
    } catch (e: any) {
        console.error(`Failed to fetch configuration`);
        toast({
            title: `Failed to fetch configuration`,
            variant: 'destructive'
        })
    }
})

watch(enableMatchConfirmation, async (value) => {
    if (initialized.value) {
        await updateConfiguration({
            enable_match_confirmation: value
        })
    }
})

watch(showOnlySundays, async (value) => {
    if (initialized.value) {
        await updateConfiguration({
            show_only_sundays: value
        })
    }
})

const updateConfiguration = async (data: any) => {
    try {
        const response = await fetch(`http://localhost:5003/api/settings`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            body: JSON.stringify(data),
        })
        return response
    } catch (e: any) {
        console.error(`Failed to update configuration: ${data}`);
        toast({
            title: `Failed to update configuration`,
            variant: 'destructive'
        });
    }
}
</script>

<style scoped></style>
