'use client'

import { useEffect, useState } from 'react'
import { useRouter, usePathname } from 'next/navigation'
import Link from 'next/link'

export default function AuthButtons() {
  const router = useRouter()
  const pathname = usePathname()
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [userEmail, setUserEmail] = useState('')

  useEffect(() => {
    // 로그인 상태 확인
    const token = localStorage.getItem('access_token')
    const email = localStorage.getItem('user_email')
    setIsLoggedIn(!!token)
    setUserEmail(email || '')
  }, [pathname])

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user_email')
    setIsLoggedIn(false)
    setUserEmail('')
    router.push('/')
  }

  if (isLoggedIn) {
    return (
      <div className="flex items-center space-x-3 ml-2">
        <span className="text-sm text-slate-600 hidden lg:inline">{userEmail}</span>
        <button
          onClick={handleLogout}
          className="px-4 py-2 bg-slate-200 text-slate-700 rounded-lg hover:bg-slate-300 transition-colors font-medium"
        >
          로그아웃
        </button>
      </div>
    )
  }

  return (
    <div className="flex items-center space-x-2 ml-2">
      <Link
        href="/login"
        className="px-4 py-2 text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-lg transition-colors font-medium"
      >
        로그인
      </Link>
      <Link
        href="/register"
        className="px-4 py-2 bg-primary-600 text-white hover:bg-primary-700 rounded-lg transition-colors font-medium"
      >
        회원가입
      </Link>
    </div>
  )
}
