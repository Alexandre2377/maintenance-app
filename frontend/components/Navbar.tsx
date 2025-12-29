'use client'

import Link from 'next/link'
import { useRouter, usePathname } from 'next/navigation'
import { useEffect, useState } from 'react'

export default function Navbar() {
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

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* 로고/홈 링크 */}
          <Link href="/" className="flex items-center">
            <span className="text-xl font-bold text-primary-600">건물 유지보수</span>
          </Link>

          {/* 네비게이션 링크 */}
          <div className="hidden md:flex items-center space-x-8">
            <Link
              href="/submit"
              className="text-gray-700 hover:text-primary-600 font-medium transition-colors"
            >
              요청하기
            </Link>
            <Link
              href="/dashboard"
              className="text-gray-700 hover:text-primary-600 font-medium transition-colors"
            >
              대시보드
            </Link>

            {/* 인증 버튼 */}
            {isLoggedIn ? (
              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-600">{userEmail}</span>
                <button
                  onClick={handleLogout}
                  className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 font-medium transition-colors"
                >
                  로그아웃
                </button>
              </div>
            ) : (
              <div className="flex items-center space-x-3">
                <Link
                  href="/login"
                  className="px-4 py-2 text-gray-700 hover:text-primary-600 font-medium transition-colors"
                >
                  로그인
                </Link>
                <Link
                  href="/register"
                  className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 font-medium transition-colors"
                >
                  회원가입
                </Link>
              </div>
            )}
          </div>

          {/* 모바일 메뉴 (간단 버전) */}
          <div className="md:hidden flex items-center space-x-2">
            <Link
              href="/submit"
              className="px-3 py-2 text-sm text-gray-700 hover:text-primary-600"
            >
              요청
            </Link>
            <Link
              href="/dashboard"
              className="px-3 py-2 text-sm text-gray-700 hover:text-primary-600"
            >
              대시보드
            </Link>
            {isLoggedIn ? (
              <button
                onClick={handleLogout}
                className="px-3 py-2 text-sm bg-gray-200 text-gray-700 rounded-lg"
              >
                로그아웃
              </button>
            ) : (
              <Link
                href="/login"
                className="px-3 py-2 text-sm bg-primary-600 text-white rounded-lg"
              >
                로그인
              </Link>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}
