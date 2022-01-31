export interface Task{
  name: string
  description: string
}

export interface Equipment {
  name: string
  tasks: Task[]
  description: string
}
