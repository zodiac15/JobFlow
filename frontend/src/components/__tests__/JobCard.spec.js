/**
 * @vitest-environment jsdom
 */
import { mount, RouterLinkStub } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import JobCard from '../JobCard.vue'

describe('JobCard.vue', () => {
    it('renders job details correctly', () => {
        const job = {
            id: 1,
            title: 'Software Engineer',
            company: 'Tech Corp',
            location: 'Remote',
            source: 'LinkedIn',
            date_posted: new Date().toISOString()
        }

        const wrapper = mount(JobCard, {
            props: { job },
            global: {
                stubs: {
                    'router-link': RouterLinkStub
                }
            }
        })

        expect(wrapper.text()).toContain('Software Engineer')
        expect(wrapper.text()).toContain('Tech Corp')
        expect(wrapper.text()).toContain('Remote')
        expect(wrapper.text()).toContain('LinkedIn')
    })
})
